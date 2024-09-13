#Azure Automation String Variable name for your Storage Account Key
$storageKeyVariableName = "STORAGEKEYVARIABLENAME";
#Name of your Storage Account
$storageAccountName = "STORAGEACCOUNTNAME";
#Name of your Storage Container
$storageContainerName = "STORAGECONTAINERNAME";
# Set the number of days that you want the blob to be stored for.
$retentionInDays = 30


# Get the storage key
$storageKey = Get-AutomationVariable -Name $storageKeyVariableName;
# Set up the storage context for the storage account.
$context = New-AzureStorageContext -StorageAccountName $storageAccountName -StorageAccountKey $storageKey
# Get all of the blobs in the storage account.
$blobs = Get-AzureStorageBlob -Container $storageContainerName -Context $context


foreach($blob in $blobs)
{
    # Get the current time to compare to the time that the blob was created.
	$currentTime = Get-Date;
    # If the blob is more than $retentionInDays old, delete it.
	if(($currentTime - $blob.LastModified.DateTime).TotalDays -gt $retentionInDays)
	{
		echo ("Deleting blob " + $blob.Name)
        # Delete the blob.e
		Remove-AzureStorageBlob -Container $storageContainerName -Context $context -Blob $blob.Name;
	}
}
