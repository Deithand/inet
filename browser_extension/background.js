chrome.downloads.onCreated.addListener((downloadItem) => {
  // We get the download URL from the downloadItem object
  const downloadUrl = downloadItem.url;

  // Cancel the browser's download
  chrome.downloads.cancel(downloadItem.id);

  // Send the URL to the Python application
  fetch('http://localhost:8080/add_download', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ url: downloadUrl }),
  })
  .then(response => {
    if (!response.ok) {
      console.error('Failed to send download to application.');
    }
  })
  .catch(error => {
    console.error('Error communicating with the download manager application.', error);
    // Notify the user that the application is not running
    chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icon48.png', // we'll need to create an icon later
        title: 'Download Manager',
        message: 'Could not connect to the desktop application. Is it running?'
    });
  });
});
