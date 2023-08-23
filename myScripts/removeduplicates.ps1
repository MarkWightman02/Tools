#Path to folder
$directoryPath = "C:\"

# Get all photos, change file type as needed
$imageFiles = Get-ChildItem -Path $directoryPath -File | Where-Object { $_.Extension -match '\.(jpg|jpeg|png|gif)$' }

# Create a hashtable to keep track of seen file hashes
$hashTable = @{}

# Loop through the image files
foreach ($file in $imageFiles) {
    # Get the hash
    $hash = (Get-FileHash -Path $file.FullName).Hash

    # Check if the hash is already in the hashtable
    if ($hashTable.ContainsKey($hash)) {
        Write-Host "Duplicate found: $($file.FullName)"
        
        Remove-Item -Path $file.FullName -Force
    } else {
        $hashTable[$hash] = $file.FullName
    }
}

Write-Host "Duplicate removal completed."
