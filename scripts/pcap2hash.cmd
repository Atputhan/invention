@echo off
rem pcap2hash.cmd - windows wrapper
setlocal
set PCAP=%~1
if "%PCAP%"=="" (
  echo usage: pcap2hash.cmd ^<input.pcapng^> [output.22000]
  exit /b 1
)
set OUT=%~2
if "%OUT%"=="" set OUT=%~dpn1.22000
python "%~dp0pcapng_to_22000.py" --beacon-info "%PCAP%" "%OUT%"
endlocal
