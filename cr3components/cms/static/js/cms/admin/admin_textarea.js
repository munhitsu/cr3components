$(document).ready(function() {
    $("textarea").wymeditor({
        updateSelector: "input:submit",
        updateEvent:    "click",
        skin: 'default',
        logoHtml:'',
        classesItems: [
          {'name': 'node-text-mark', 'title': 'mark it', 'expr': '*'}
        ],
    });
});
