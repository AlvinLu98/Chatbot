$(document).ready(_ => {
    $('#user_chat').submit(function(e) {
        // https://stackoverflow.com/questions/47950852/preventdefault-wont-stop-the-page-from-refreshing

        e.preventDefault();
        const input_mes = $('#chatbox').val();
        $('#chatInfo').append(`
    <div class="user_message" align="right">
        ${input_mes}
    </div>
    `)
        $('#chatbox').val('')
        $('#chatbox').prop('disabled', true)
        $('#chatInfo').append(`
    <div class="bot_response" id="loading">
        ......
    </div>
    `)
        process_message(input_mes)
    })

    // https://stackoverflow.com/questions/28415178/how-do-you-show-the-current-time-on-a-web-page
    $(function() {
        var clockElement = document.getElementById("clock")

        function updateClock(clock) {
            clock.innerHTML = new Date().toLocaleString();
        }

        setInterval(function() {
            updateClock(clockElement);
        }, 1000);

    }());
})

function process_message(message) {
    $.post("/message", { message: message }, data => {
        $("#loading").remove();
        $('#chatInfo').append(`
        <div class="bot_response">
            ${data.message}
        </div>
        `)
        $('#chatbox').prop('disabled', false)
    })
}