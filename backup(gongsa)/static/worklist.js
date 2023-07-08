function handleEditButtonClick(postId) {
    // Construct the URL for the edit page using the post ID
    var editUrl = '/gongsa/update/' + postId + '/';
  
    // Redirect to the edit page
    window.location.href = editUrl;
  }