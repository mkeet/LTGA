var React = require('react');

var MultiAnswer = React.createClass({
    getInitialState: function() {
        if (this.props.answers) {
            this.props.answers.push('');
            return { answers: this.props.answers};
        }
        return { answers: [''] };
    },
    genHandleChange: function(event) {
        var index = parseInt(event.target.attributes.getNamedItem('data-key').value);
        this.state.answers[index] = event.target.value;
        if (index + 1 == this.state.answers.length) {
            this.state.answers.push('');
        }
        this.setState({answers: this.state.answers});
    },
    inputStyle: {
        marginTop: '5px',
        marginBottom: '5px',
        width: '80%'
    },
    render: function() {
        return (<div>
                {this.state.answers.map(function(value, index) {
                    return (
                    <div key={index} >
                        <input
                            style={this.inputStyle}
                            data-key={index}
                            placeholder={"Enter a possible answer"}
                            className="form-control"
                            type="text" 
                            name={"answer"+index}
                            value={value} 
                            onChange={this.genHandleChange} />
                    </div>);
                }.bind(this))}
            </div>);
    }
});


var QuestionEditor = React.createClass({
    getInitialState: function() {
        return {'question': this.props.question ? this.props.question : ''};
    },
    onQuestionChange: function(event) {
        this.setState({'question': event.target.value});
    },
    render: function() {
    return (<div className="">
        <h2 className="form-signin-heading">So you want to create a question hey?</h2>
        <input 
            type="text" 
            className="form-control" 
            name="question" 
            placeholder="Enter a question" 
            value={this.state.question}
            onChange={this.onQuestionChange}/>
        Attach an image: <input name="question-image" type="file"></input>
        {/*<div data-toggle="buttons">
            <label htmlFor="multiple-choice" className="btn btn-default active" style={{width: '48%'}}>
                Multiple Choice
                <input  name="multiple-choice" checked="checked" type="radio"></input>
            </label>
            <label htmlFor="open-ended" className="btn btn-default" style={{width: "48%"}}>
                Open Ended
                <input name="open-ended" type="radio"></input>
            </label>
        </div>*/}
        <div id="answer-list"><MultiAnswer answers={this.props.answers}/></div>
        <input 
            className="form-control btn btn-block btn-primary" 
            type="submit" 
            value="Add Question" />
    </div>);
    }
});


function renderQuestionEditor(questions, answers, container) {
    React.render(
        <QuestionEditor 
        question={questions}
        answers={answers}
        />, container);
}

module.exports = {
    MultiAnswer: MultiAnswer,
    QuestionEditor: QuestionEditor,
    renderQuestionEditor: renderQuestionEditor
};
