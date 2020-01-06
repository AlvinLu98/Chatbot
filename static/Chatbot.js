$(document).ready(_ => {
    $('#user_chat').submit(function(e) {
        // https://stackoverflow.com/questions/47950852/preventdefault-wont-stop-the-page-from-refreshing

        e.preventDefault();
        const input_mes = $('#chatbox').val();
        $('#chatInfo').append(`
    <div class="user-message" align="right">
        ${input_mes}
    </div>
    `)
        $('#chatbox').val('')
        process_message(input_mes)
    })
})

function process_message(message) {
    $.post("/message", { message: message }, data => {
        $('#chatInfo').append(`
    <div class="bot-response">
        ${data.message}
    </div>
`)
    })
}