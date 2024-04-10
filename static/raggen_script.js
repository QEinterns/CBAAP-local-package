document.getElementById('file-container').addEventListener('click', function() {
    document.getElementById('files').click();
  });
  
  document.getElementById('files').addEventListener('change', function() {
    const fileCountSpan = document.getElementById('file-count');
  
    if (this.files && this.files.length > 0) {
      fileCountSpan.textContent = this.files.length + ' files selected';
    } else {
      fileCountSpan.textContent = '0 files selected';
    }
  });
  
  // Prevent label click from triggering file input click
  document.getElementById('files').addEventListener('click', function(event) {
    event.stopPropagation();
  });
  