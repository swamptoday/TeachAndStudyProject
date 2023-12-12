// Initialize evo-calendar in your script file or an inline <script> tag
$(document).ready(function() {
    $('#calendar').evoCalendar({
        settingName: "hello",
        calendarEvents:[
            {
                id:'mmnnn',
                name:'new year',
                description: "Author's note: Thank you for using EvoCalendar! :)",
                date:'12/1/2023',
                type:'event',            
            },
            {
                id:'0908',
                name:'new year',
                date:'January/1/2020',
                type:'holiday',
                everyYear:true
            
            }
        ]
    })
})

/*
$('#calendar').evoCalendar('calendarEvents', {
        'calendarEvents': [
        {
        id: '4hducye', // Event's id (required, for removing event)
        description: 'Lorem ipsum dolor sit amet..', // Description of event (optional)
        badge: '1-day event', // Event badge (optional)
        date: new Date(), // Date of event
        type: 'holiday', // Type of event (event|holiday|birthday)
        color: '#63d867', // Event custom color (optional)
        everyYear: true // Event is every year (optional)
        }
        ]
    });
*/