$(document).ready(function() {
    const modeSelector = $('#conversionMode');
    const fileLabel = $('#fileLabel');
    const languageSection = $('.language-selection');
    const progressBar = $('.progress-bar');
    const progressText = $('#progressText');
    let currentSessionId = null;
    
    // Handle mode change
    modeSelector.change(function() {
        const mode = $(this).val();
        if (mode === 'pdf') {
            fileLabel.text('Select PDF Files');
            languageSection.show();
            $('#files').attr('accept', '.pdf');
        } else {
            fileLabel.text('Select Image Files');
            languageSection.hide();
            $('#files').attr('accept', '.jpg,.jpeg,.png,.bmp,.tiff');
        }
    });

    // Drag and drop handlers
    $('.card').on('dragover', function(e) {
        e.preventDefault();
        $(this).addClass('dragover');
    });

    $('.card').on('dragleave', function(e) {
        e.preventDefault();
        $(this).removeClass('dragover');
    });

    $('.card').on('drop', function(e) {
        e.preventDefault();
        $(this).removeClass('dragover');
        const files = e.originalEvent.dataTransfer.files;
        $('#files')[0].files = files;
        updateFileList(files);
    });

    // File input change handler
    $('#files').change(function() {
        updateFileList(this.files);
    });

    // Form submission handler
    $('#uploadForm').submit(function(e) {
        e.preventDefault();
        const files = $('#files')[0].files;
        const mode = $('#conversionMode').val();
        const lang = $('#language').val();
        
        if (files.length === 0) {
            showError(`Please select at least one ${mode === 'pdf' ? 'PDF' : 'image'} file`);
            return;
        }

        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }
        formData.append('lang', lang);
        formData.append('mode', mode);

        uploadFiles(formData);
    });

    function uploadFiles(formData) {
        // Reset UI
        progressBar.css('width', '0%')
            .removeClass('bg-success')
            .addClass('progress-bar-animated');
        progressText.text('Starting upload...');
        $('#downloadSection').hide();

        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                currentSessionId = response.session_id;
                startProcessing(response.session_id, response.mode, response.lang);
            },
            error: function(xhr) {
                showError(xhr.responseJSON?.error || 'Upload failed');
            }
        });
    }

    function startProcessing(sessionId, mode, lang) {
        checkProgress(sessionId);
        $.get(`/process/${sessionId}/${mode}/${lang}`)
            .fail(function(xhr) {
                showError(xhr.responseJSON?.error || 'Processing failed to start');
            });
    }

    function checkProgress(sessionId) {
        let attempts = 0;
        const maxAttempts = 30; // 30 seconds timeout
        const checkInterval = 1000; // 1 second

        const poll = function() {
            $.get(`/progress/${sessionId}`)
                .done(function(response) {
                    if (response.error) {
                        showError(response.error);
                        return;
                    }

                    const progressPercent = response.progress;
                    const current = response.current;
                    const total = response.total;

                    // Update progress display
                    progressBar.css('width', progressPercent + '%');
                    progressText.text(`${progressPercent}% Complete (${current}/${total} files processed)`);

                    if (current < total) {
                        setTimeout(poll, checkInterval);
                    } else {
                        // Processing complete
                        progressBar.removeClass('progress-bar-animated')
                            .addClass('bg-success');
                        $('#downloadLink').attr('href', `/download/${sessionId}`);
                        $('#downloadSection').show();
                    }
                })
                .fail(function(xhr) {
                    if (xhr.status === 404 && attempts < maxAttempts) {
                        attempts++;
                        setTimeout(poll, checkInterval);
                    } else {
                        showError(xhr.responseJSON?.error || 'Error checking progress');
                    }
                });
        };

        poll();
    }

    function updateFileList(files) {
        const fileList = Array.from(files).map(f => f.name).join('\n');
        progressText.html(`
            <strong>Selected Files (${files.length}):</strong>
            <div class="mt-2 text-muted">${fileList}</div>
        `);
    }

    function showError(message) {
        progressBar.removeClass('progress-bar-animated')
            .css('width', '100%')
            .addClass('bg-danger');
        progressText.html(`<div class="alert alert-danger">${message}</div>`);
    }

    // Handle page refresh
    $(window).on('beforeunload', function() {
        if (currentSessionId) {
            // Clean up session on page refresh
            $.ajax({
                url: `/cleanup/${currentSessionId}`,
                type: 'DELETE',
                async: false // Ensure request completes before page unloads
            });
        }
    });
});