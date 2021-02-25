var React = require('react');
var update = require('react/lib/update');
var DragDropContext = require('react-dnd').DragDropContext;
var DragSource = require('react-dnd').DragSource;
var DropTarget = require('react-dnd').DropTarget;
var HTML5Backend = require('react-dnd/modules/backends/HTML5')
var $ = require('jQuery');

var ItemTypes = {
    Question: 'QUESTION',
    Group: 'GROUP'
};

function dropCollect(connect, monitor) {
    return {
        connectDropTarget: connect.dropTarget(),
        isOver: monitor.isOver()
    };
}

function collect(connect, monitor) {
  return {
    connectDragSource: connect.dragSource(),
    isDragging: monitor.isDragging(),
  };
}

var QuestionRowSpec = {
    beginDrag: function(props) {
        return props.question;
    }
};

function handleDragging(dropped, props, monitor) {
    var draggedQuestion = monitor.getItem();
    var droppedQuestion = props.question;
    if (draggedQuestion.id != droppedQuestion.id || draggedQuestion.group_id != droppedQuestion.group_id) {
        props.moveRow(dropped, draggedQuestion, droppedQuestion);
    }
}

var QuestionTarget = {
    drop: function(props, monitor) {
         handleDragging(true, props, monitor);
    },
    hover: function(props, monitor) {
         handleDragging(false, props, monitor);
    },
};

var QuestionRow = 
    DragSource(ItemTypes.Question, QuestionRowSpec, collect)
    (DropTarget(ItemTypes.Question, QuestionTarget, dropCollect)
    (React.createClass({
        propTypes: {
            connectDragSource: React.PropTypes.func.isRequired,
            connectDropTarget: React.PropTypes.func.isRequired,
            moveRow: React.PropTypes.func.isRequired,
            isDragging: React.PropTypes.bool.isRequired,
            question: React.PropTypes.any.isRequired
        },
        render: function() {
            if (this.props.question.id == -1) {
                return this.props.connectDropTarget(<li className="list-group-item">
                    <i>Drop here</i>
                </li>);
            }
            var opacity = this.props.isDragging?0:1;
            var expired = this.props.question.expired?'Closed':'Open';
            var progress = this.props.progress ? <i className="fa fa-spinner fa-spin"></i> : null;
            return this.props.connectDragSource(
                   this.props.connectDropTarget(
                <li className="list-group-item" style={{opacity:opacity}}>
                    <div className="row">
                        <div className="col-md-3">
                            <a href={"/question/"+this.props.question.id}>
                                { this.props.question.question}
                            </a>
                        </div>
                        <div className="col-md-3">
                            {this.props.question.responses}
                        </div>
                        <div className="col-md-3">
                            {this.props.question.created_at}
                        </div>
                        <div className="col-md-3">
                            {expired}
                        </div>
                        {progress}
                    </div>
                </li>));
        }
    }
)));

var GroupRowSpec = {
    beginDrag: function(props) {
        return {
            group: props.group
        };
    }
};

function handleGroupMove(drop, props, monitor) {
    var draggedGroup = monitor.getItem().group;
    var droppedGroup = props.group;
    if (draggedGroup.id != droppedGroup.id || draggedGroup.group_id != droppedGroup.group_id) {
        props.moveGroup(drop, draggedGroup, droppedGroup);
    }
}

var GroupTarget = {
    drop: handleGroupMove,
    hover: handleGroupMove
};

var GroupRow = 
    DragSource(ItemTypes.Group, GroupRowSpec, collect)
    (DropTarget(ItemTypes.Group, GroupTarget, dropCollect)
    (React.createClass({
        propTypes: {
            connectDragSource: React.PropTypes.func.isRequired,
            connectDropTarget: React.PropTypes.func.isRequired,
            moveRow: React.PropTypes.func,
            moveGroup: React.PropTypes.func.isRequired,
            isDragging: React.PropTypes.bool.isRequired,
            group: React.PropTypes.any.isRequired,
            questions: React.PropTypes.any.isRequired
        },
        getInitialState: function() {
            return {
                collapsed: false
            };
        },
        renderQuestions() {
            var questions = this.props.questions;
            questions.unshift({id:-1});
            return questions.map(function(question) {
                if (question.id == -1) {
                    return (<QuestionRow
                        key={this.props.group.id+"placeholder"}
                        question={{id:-1, group_id: this.props.group.id}}
                        moveRow={this.props.moveRow}
                        />);
                }
                return this.props.connectDropTarget(
                        <QuestionRow 
                        moveRow={this.props.moveRow}
                        key={question.question} 
                        question={question} />);
            }.bind(this));
        },
        handleHeadingClicked: function() {
            this.setState({
                collapsed: !this.state.collapsed
            });
        },
        render: function() {
            var opacity = this.props.isDragging?0:1;

            return this.props.connectDragSource(
                   this.props.connectDropTarget(
                <li className="list-group-item" style={{opacity:opacity}}>
                    <b>
                        <a onClick={this.handleHeadingClicked}>
                            { this.props.group.name}
                        </a>
                    </b>
                    <ul>
                        {this.state.collapsed ? null : this.renderQuestions()}
                    </ul>
                </li>));
        }
    })));

var QuestionList = React.createClass({
    propTypes: {
        // list of groups containing questions
        // [{
        //  group_id: 5,
        //  group_name: 'what is your name?
        //  questions: [{}]
        // }]
        groups: React.PropTypes.any.isRequired,
        questions: React.PropTypes.any.isRequired
    },
    getInitialState: function() {
        return {
            groups: this.props.groups,
            questions: this.props.questions
        };
    },
    render: function() {
        var moveRow = this.moveRow;
        var moveGroup = this.moveGroup;
        var all_questions = this.state.questions;
        return (
            <div>
                <NewGroupButton
                   newGroup={this.newGroupHandler} />
                <ul>
                    <div className="row">
                        <div className="col-md-3">
                            <b>Question</b>
                        </div>
                        <div className="col-md-3">
                        <b>Number of Responses</b>
                        </div>
                        <div className="col-md-3">
                            <b>Created At</b>
                        </div>
                        <div className="col-md-3">
                            <b>Status</b>
                        </div>
                    </div>
                {
                this.state.groups.map(function(group) {
                    var questions = all_questions.filter(
                        function(q) { return q.group_id == group.id; });
                    return <GroupRow 
                        moveRow={moveRow}
                        moveGroup={moveGroup}
                        key={group.id}
                        group={group}
                        questions={questions}
                        />;
                    })
                }
                </ul>
            </div>
            );
    },
    newGroupHandler: function(group) {
        this.setState(update(this.state, {
            groups: {
                $push: [
                    group
                ]
            }
        }));
    },
    moveGroup: function(draggedGroup, droppedGroup) {
        var groups = this.state.groups;
        // update indices
        var index1 = groups.indexOf(draggedGroup);
        var index2 = groups.indexOf(droppedGroup);
        var q1 = groups[index1];
        var q2 = groups[index2];

        this.setState(update(this.state, {
            groups: {
                $splice: [
                    [index1, 1],
                    [index2, 0, q1]
                ]
            }
        }));
    },
    moveRow: function(dropped, draggedRow, droppedRow) {
        console.log('moveRow');
        console.log(droppedRow);
        // XXX stupid hacks 
        /*if (dropped) {
            this.setState({
                droppedRow: null
            });
        } else {
            if (!this.state.droppedRow) {
                this.setState({
                    droppedRow: droppedRow
                });
            }
            droppedRow = this.state.droppedRow;
        }*/
        var questions = this.state.questions;
        // update indices
        var index1 = questions.indexOf(draggedRow);
        var index2;
        var new_group = false;
        var q1 = questions[index1];
        q1.group_id = droppedRow.group_id;
        // mark the current question as "in progress"
        q1.progress = true;

        var drop_id;
        if (droppedRow.id != -1) {
            console.log('dropped row is not -1');
            var index2 = questions.indexOf(droppedRow);
            var q2 = questions[index2];
            drop_id = q2.id;
        } else {
            // we have dropped into a new non-existant group
            new_group = true;
            drop_id = droppedRow.group_id;
            index2 = index1;
            this.setState(update(this.state, {
                questions: {
                    $splice: [
                        [index1, 1, q1]
                    ]
                }
            }));
        }
        console.log(droppedRow.id);
        console.log(new_group);

        var type = new_group ? 'new_group_question' : 'question';
        this.moveQuery(type, q1.id, drop_id, function(data, statusCode) {
            console.log(statusCode);
            q1.progress = false;
            /*this.setState(update(this.state, {
                questions: {
                    $splice: [
                        [index2, 1, q1]
                    ]
                }
            }));*/
        });
        if (!new_group) {
            this.setState(update(this.state, {
                questions: {
                    $splice: [
                        [index1, 1],
                        [index2, 0, q1]
                    ]
                }
            }));
        }
    },
    moveQuery: function(type, from_id, to_id, callback) {
        console.log(type);
        $.post(
            '/admin/order',
            {
                type: type,
                from_id: from_id,
                to_id: to_id
            },
            callback,
            'json'
        );
    }
});

var NewGroupButton = React.createClass({
    propTypes: {
        newGroup: React.PropTypes.func.isRequired
    },
    getInitialState: function() {
        return {
            group_name: '',
            showing_group: false,
            submitting: false
        };
    },
    handleButtonClick: function() {
        this.setState({
            showing_group: true
        });
    },
    handleNameChange: function(event) {
        this.setState({group_name: event.target.value});
    },
    handleNameSubmit: function() {
        this.setState({submitting: true});
        $.post(
            '/admin/group/create',
            {
                group_name: this.state.group_name
            },
            function(data, statusCode) {
                this.setState({
                    showing_group: false,
                    group_name: '',
                    submitting: false
                });
                this.props.newGroup(data);
            }.bind(this),
            'json'
        );
    },
    render: function() {
        var group_input = null;
        if (this.state.showing_group) {
            group_input = <div>
                <input 
                    type="text" 
                    name="new_group" 
                    value={this.state.group_name} 
                    onChange={this.handleNameChange}
                    placeholder="New Group name" />
                <a onClick={this.handleNameSubmit}>Create Group</a>
            </div>
        } else {
            group_input = <a onClick={this.handleButtonClick}>Create a New Group</a>;
        }
        var progress = null;
        if (this.state.submitting) {
            progress = <i className="fa fa-spinner fa-spin"></i>;
        }
        return <div>
                {group_input}
                {progress}
            </div>;
    }

});

function renderQuestionList(groups, questions, container) {
    return React.render(
        (<div>
            <QuestionList
                groups={groups}
                questions={questions} />
        </div>),
        container);
}

QuestionList = DragDropContext(HTML5Backend)(QuestionList);
module.exports = {
    QuestionRow: QuestionRow,
    GroupRow: GroupRow,
    QuestionList: QuestionList,
    renderQuestionList: renderQuestionList
};
