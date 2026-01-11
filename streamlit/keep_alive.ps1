# keep_alive.ps1
# This script visits the Streamlit app URL to prevent it from hibernating.
# It logs the result to a file in the same directory.

$Url = "https://qr-greeting.streamlit.app/?tab=scan"
$LogFile = Join-Path -Path $PSScriptRoot -ChildPath "keep_alive_log.txt"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

try {
    # Send a HEAD request effectively "pings" the server without downloading the full body
    # If Streamlit needs a GET to count as activity, we use GET.
    # header User-Agent helps mimic a real browser to ensure the request is counted
    $Response = Invoke-WebRequest -Uri $Url -Method Get -UseBasicParsing -UserAgent "Mozilla/5.0 (KeepAliveScript)" -ErrorAction Stop
    
    $Message = "[$Timestamp] SUCCESS: Pinged $Url (Status: $($Response.StatusCode))"
    Write-Output $Message
    Add-Content -Path $LogFile -Value $Message
}
catch {
    $Message = "[$Timestamp] ERROR: Failed to ping $Url. Details: $_"
    Write-Error $Message
    Add-Content -Path $LogFile -Value $Message
    
    # Optional: If you WANT the browser to open on error (or always), uncomment the line below:
    # Start-Process $Url
}
