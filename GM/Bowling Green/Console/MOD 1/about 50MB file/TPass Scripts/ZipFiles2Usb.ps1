Add-Type -AssemblyName PresentationCore,PresentationFramework,System.Windows.Forms

$ScriptDir = Split-Path $script:MyInvocation.MyCommand.Path

# Change the current directory to the parent folder
cd $ScriptDir\..

$appPath = pwd
$logPath = "$appPath\Logs"
$tempLogPath = "$appPath\TempLogs"
$configPath = "$appPath\Configuration"
$testAppScriptsPath = "$appPath\Test App Scripts"
$tpassScriptsPath = "$appPath\TPass Scripts"

# Initialize the number of days to be zipped
$days = -10

# Keep reducing the number of days to be zipped until the size is below the threshold
do 
{
    # Get the size of all log files to be zipped
    $size = ls -r -File "$logPath" | where {$_.LastWriteTime -ge (Get-Date).AddDays($days)} | measure -s Length
	if ($days -eq 0)
	{
		Write-Host "The size of all files exceeded the maximum size, so all files changed since yesterday will be backed up"
		break
	}
	else
	{
		Write-Host "# of days to be zipped =" (-$days) "- Size =" $size.Sum
	}
    $days++
} while ($size.Sum -gt 15000000)

$days--

# Get the mapped drive for the USB
$USBDrive = Get-WmiObject Win32_Volume -Filter ("DriveType={0}" -f [int][System.io.Drivetype]::removable)

while (!$USBDrive.Name) # Keep looping until USG was plugged in or user hits Cancel
{
    $resp = [System.Windows.MessageBox]::Show('Please insert the USB drive','Zipping Files to USB','OKCancel','Error')
    
    if ($resp -eq "Cancel")
    {
        Write-Host "Operation aborted"
        exit
    }
    $USBDrive = Get-WmiObject Win32_Volume -Filter ("DriveType={0}" -f [int][System.io.Drivetype]::removable)
}

# Name of the zip file on the USB
$USBZipFile = $USBDrive.Name + (HOSTNAME.EXE) + '-' + (Get-Date).ToString('yyyy-MM-dd HH.mm.ss') + ".zip"
$localZipFile = [System.IO.Path]::GetTempFileName() + ".zip"

New-Item -Path "$tempLogPath" -ItemType "directory" -Force

# Copy the selected log files to a temporary folder as NLog locks them
if (ls -r -File "$logPath" | where {$_.LastWriteTime -ge (Get-Date).AddDays($days)}) {
    ls -r -File "$logPath" | 
        where {$_.LastWriteTime -ge (Get-Date).AddDays($days)} | 
        Copy-Item  -Destination  "$tempLogPath" -Force
}

# Compress the selected log files
if (ls -r -File "$tempLogPath" | where {$_.LastWriteTime -ge (Get-Date).AddDays($days)}) {
    ls -r -File "$tempLogPath" | 
        where {$_.LastWriteTime -ge (Get-Date).AddDays($days)} | 
        Compress-Archive -CompressionLevel Optimal -ErrorAction SilentlyContinue -DestinationPath "$localZipFile" -Force
}

Remove-Item "$tempLogPath" -Recurse -Force

# Compress the files in the Configuration folder
if (ls -r $configPath) {
    Compress-Archive -CompressionLevel Optimal -ErrorAction SilentlyContinue -DestinationPath "$localZipFile" -Path "$configPath" -Update
}

# Compress the files in the Test App Scripts folder
if (ls -r $testAppScriptsPath) {
    Compress-Archive -CompressionLevel Optimal -ErrorAction SilentlyContinue -DestinationPath "$localZipFile" -Path "$testAppScriptsPath" -Update
}

# Compress the files in the TPass Scripts folder
if (ls -r $tpassScriptsPath) {
    Compress-Archive -CompressionLevel Optimal -ErrorAction SilentlyContinue -DestinationPath "$localZipFile" -Path "$tpassScriptsPath" -Update
}

# Copy the working zip file to the USB
Copy-Item -Path $localZipFile -Destination $USBZipFile
if (Test-Path -Path $USBZipFile) {
	# Notify user of the final zip file location
	$resp = [System.Windows.MessageBox]::Show("Logs files were saved in $USBZipFile.",'Zipping Files to USB','OK','Information')
    Remove-Item $localZipFile
} else {
	$resp = [System.Windows.MessageBox]::Show("Failed to zip log files!`nPlease try again.",'Zipping Files to USB','OK','Error')
}