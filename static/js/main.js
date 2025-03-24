$(document).ready(function() {
    // Initialize DataTable
    $('#taskTable').DataTable({
        processing: true,
        serverSide: true,  // Enable server-side processing
        ajax: {
            url: '/api/tasks',
            type: 'GET',
            data: function(d) {
                d.page = d.start / d.length + 1;  // Calculate page number
                d.length = d.length;  // Number of tasks per page
            }
        },
        columns: [
            { data: 'id' },
            { data: 'content' },
            { data: 'category' },
            { data: 'datecreated' },
            {
                data: null,
                render: function(data) {
                    return `
                        <a href="/update/${data.id}" class="btn btn-sm btn-warning">
                            <i class="fas fa-edit"></i> Update
                        </a>
                        <button class="btn btn-sm btn-danger delete-btn" data-id="${data.id}">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    `;
                }
            }
        ],
        paging: true,  // Enable pagination
        pageLength: 10,  // Default number of tasks per page
        lengthMenu: [10, 25, 50, 100]  // Dropdown for tasks per page
    });

    // Handle delete button clicks
    $('#taskTable').on('click', '.delete-btn', function() {
        const taskId = $(this).data('id');
        if (confirm('Are you sure you want to delete this task?')) {
            $.ajax({
                url: `/delete/${taskId}`,
                method: 'GET',
                success: function() {
                    $('#taskTable').DataTable().ajax.reload();  // Reload DataTable
                },
                error: function(xhr, status, error) {
                    alert('Error deleting task: ' + error);
                }
            });
        }
    });
});