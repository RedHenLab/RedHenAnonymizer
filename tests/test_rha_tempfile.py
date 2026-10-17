import os
import sys
import tempfile
from unittest import mock
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import rha
import rha_quick_hack_x264_peter


class DummyArgs:
    def __init__(self, inpath, outpath, anonymize='audio', visual_anonymization=None, facepath=""):
        self.inpath = inpath
        self.outpath = outpath
        self.anonymize = anonymize
        self.visual_anonymization = visual_anonymization
        self.facepath = facepath
        self.pitch = 3.0
        self.distortion = 0.0
        self.echo = 0.8
        self.cpu_only = True
        self.hider_shape = 'rect'
        self.openpose_blending = False
        self.openpose_bind = ''
        self.openpose_container = ''
        self.openpose_modelfolder = ''
        self.openpose_keypoints = ''
        self.pdb = False


def test_rha_tempfile_lifecycle_and_cleanup(tmp_path):
    """Verify that tempfile.TemporaryDirectory is used and cleaned up on success."""
    input_file = tmp_path / "sample_input.wav"
    input_file.write_text("dummy audio data")
    output_file = tmp_path / "sample_output.wav"

    args = DummyArgs(str(input_file), str(output_file), anonymize='audio')

    captured_temp_dirs = []
    original_temp_dir = tempfile.TemporaryDirectory

    def tracking_temp_dir(*t_args, **t_kwargs):
        ctx = original_temp_dir(*t_args, **t_kwargs)
        captured_temp_dirs.append(ctx.name)
        return ctx

    mock_metadata = {
        'streams': [
            {'codec_type': 'audio', 'start_time': '0.0'}
        ]
    }

    with mock.patch('tempfile.TemporaryDirectory', side_effect=tracking_temp_dir), \
         mock.patch('ffmpeg.probe', return_value=mock_metadata), \
         mock.patch('subprocess.call', return_value=0), \
         mock.patch('os.system', return_value=0):

        rha.main(args)

    assert len(captured_temp_dirs) == 1
    temp_dir_path = captured_temp_dirs[0]

    # Verify temp dir used the expected prefix
    assert os.path.basename(temp_dir_path).startswith("anon_tmp_")
    # Verify the temporary directory was created inside the system temp directory, not the current working directory
    assert not os.path.exists(os.path.join(os.getcwd(), os.path.basename(temp_dir_path)))
    # Verify it has been cleaned up completely after main() returns
    assert not os.path.exists(temp_dir_path)


def test_rha_tempfile_cleanup_on_exception(tmp_path):
    """Verify that the temporary directory is cleaned up even if an exception occurs."""
    input_file = tmp_path / "error_input.wav"
    input_file.write_text("dummy audio data")
    output_file = tmp_path / "error_output.wav"

    args = DummyArgs(str(input_file), str(output_file), anonymize='audio')

    captured_temp_dirs = []
    original_temp_dir = tempfile.TemporaryDirectory

    def tracking_temp_dir(*t_args, **t_kwargs):
        ctx = original_temp_dir(*t_args, **t_kwargs)
        captured_temp_dirs.append(ctx.name)
        return ctx

    with mock.patch('tempfile.TemporaryDirectory', side_effect=tracking_temp_dir), \
         mock.patch('ffmpeg.probe', side_effect=RuntimeError("Simulated probe failure")):

        with pytest.raises(RuntimeError, match="Simulated probe failure"):
            rha.main(args)

    assert len(captured_temp_dirs) == 1
    temp_dir_path = captured_temp_dirs[0]

    # Verify that the temp directory was cleaned up despite the exception
    assert not os.path.exists(temp_dir_path)


def test_rha_quick_hack_tempfile_cleanup(tmp_path, capsys):
    """Verify tempfile cleanup and TEMPDIR output for rha_quick_hack_x264_peter."""
    input_file = tmp_path / "sample_hack.wav"
    input_file.write_text("dummy audio data")
    output_file = tmp_path / "sample_hack_out.wav"

    args = DummyArgs(str(input_file), str(output_file), anonymize='audio')

    captured_temp_dirs = []
    original_temp_dir = tempfile.TemporaryDirectory

    def tracking_temp_dir(*t_args, **t_kwargs):
        ctx = original_temp_dir(*t_args, **t_kwargs)
        captured_temp_dirs.append(ctx.name)
        return ctx

    mock_metadata = {
        'streams': [
            {'codec_type': 'audio', 'start_time': '0.0'}
        ]
    }

    with mock.patch('tempfile.TemporaryDirectory', side_effect=tracking_temp_dir), \
         mock.patch('ffmpeg.probe', return_value=mock_metadata), \
         mock.patch('subprocess.call', return_value=0), \
         mock.patch('os.system', return_value=0):

        rha_quick_hack_x264_peter.main(args)

    assert len(captured_temp_dirs) == 1
    temp_dir_path = captured_temp_dirs[0]

    # Verify that the temp dir path was logged
    captured = capsys.readouterr()
    assert f"TEMPDIR: {temp_dir_path}" in captured.out
    # Verify the temporary directory is cleaned up
    assert not os.path.exists(temp_dir_path)


def test_no_cwd_pollution(tmp_path):
    """Ensure running rha does not leave anon_tmp_* folders in the current working directory."""
    input_file = tmp_path / "test.wav"
    input_file.write_text("data")
    output_file = tmp_path / "test_out.wav"

    args = DummyArgs(str(input_file), str(output_file), anonymize='audio')

    mock_metadata = {
        'streams': [
            {'codec_type': 'audio', 'start_time': '0.0'}
        ]
    }

    cwd_before = os.listdir(os.getcwd())

    with mock.patch('ffmpeg.probe', return_value=mock_metadata), \
         mock.patch('subprocess.call', return_value=0), \
         mock.patch('os.system', return_value=0):
        rha.main(args)

    cwd_after = os.listdir(os.getcwd())
    diff = set(cwd_after) - set(cwd_before)
    # Ensure no anon_tmp_* directories were created in cwd
    assert not any(item.startswith("anon_tmp_") for item in diff)


def test_rha_video_and_audio_anonymization(tmp_path):
    """Verify tempfile lifecycle when anonymizing both video and audio with face hider."""
    input_file = tmp_path / "test_av.mp4"
    input_file.write_text("dummy av content")
    output_file = tmp_path / "test_av_out.mp4"

    args = DummyArgs(
        str(input_file),
        str(output_file),
        anonymize='audiovideo',
        visual_anonymization='hider'
    )

    captured_temp_dirs = []
    original_temp_dir = tempfile.TemporaryDirectory

    def tracking_temp_dir(*t_args, **t_kwargs):
        ctx = original_temp_dir(*t_args, **t_kwargs)
        captured_temp_dirs.append(ctx.name)
        return ctx

    mock_metadata = {
        'streams': [
            {'codec_type': 'video', 'start_time': '0.0'},
            {'codec_type': 'audio', 'start_time': '0.0'}
        ]
    }

    with mock.patch('tempfile.TemporaryDirectory', side_effect=tracking_temp_dir), \
         mock.patch('ffmpeg.probe', return_value=mock_metadata), \
         mock.patch('subprocess.call', return_value=0), \
         mock.patch('os.system', return_value=0):
        rha.main(args)

    assert len(captured_temp_dirs) == 1
    assert not os.path.exists(captured_temp_dirs[0])


def test_concurrent_tempfile_isolation(tmp_path):
    """Verify that multiple instances create distinct, non-colliding temporary directories."""
    input_file = tmp_path / "shared_name.wav"
    input_file.write_text("audio data")
    out1 = tmp_path / "out1.wav"
    out2 = tmp_path / "out2.wav"

    args1 = DummyArgs(str(input_file), str(out1), anonymize='audio')
    args2 = DummyArgs(str(input_file), str(out2), anonymize='audio')

    captured_dirs = []
    original_temp_dir = tempfile.TemporaryDirectory

    def tracking_temp_dir(*t_args, **t_kwargs):
        ctx = original_temp_dir(*t_args, **t_kwargs)
        captured_dirs.append(ctx.name)
        return ctx

    mock_metadata = {
        'streams': [{'codec_type': 'audio', 'start_time': '0.0'}]
    }

    with mock.patch('tempfile.TemporaryDirectory', side_effect=tracking_temp_dir), \
         mock.patch('ffmpeg.probe', return_value=mock_metadata), \
         mock.patch('subprocess.call', return_value=0), \
         mock.patch('os.system', return_value=0):
        rha.main(args1)
        rha.main(args2)

    assert len(captured_dirs) == 2
    # Ensure they had different, non-colliding directory paths
    assert captured_dirs[0] != captured_dirs[1]
    assert not os.path.exists(captured_dirs[0])
    assert not os.path.exists(captured_dirs[1])


def test_cli_help():
    """Verify CLI interface runs and prints usage."""
    import subprocess
    result = subprocess.run(
        [sys.executable, "rha.py", "--help"],
        capture_output=True,
        text=True,
        cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    )
    assert result.returncode == 0
    assert "RHA - RedHenAnonymizer" in result.stdout

