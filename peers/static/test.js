var React = require('react');
var AdminComponents = require('./admin');

function test() {
    var questions = [
        {
            question: 'What is the complexity of binary search?',
            id: 1,
            group_id: 1
        },
        {
            question: 'What is a red black tree',
            id: 2,
            group_id: 1
        },
        {
            question: 'What does TCP IP stand for?',
            id: 1,
            group_id: 2
        },
        {
            question: 'Waht is a network?',
            id: 2,
            group_id: 2
        },
        {
            question: 'What is a social network?',
            id: 3,
            group_id: 2
        }
    ];
    var groups = [
        {
            name: 'Algorithms',
            id: 1,
        },
        {
            name: 'Networks',
            id: 2,
        }
    ];
    React.render(
        <AdminComponents.QuestionList
            groups={groups}
            questions={questions} />,
        document.getElementById('container'));
}
module.exports = test;
