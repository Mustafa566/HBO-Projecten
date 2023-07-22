// Code inspired by
// https://blog.logrocket.com/using-react-django-create-app-tutorial/

import React  from "react";
import { Button, Form, FormGroup, Input, Label } from "reactstrap";
import axios from "axios";
import { API_URL_OPEN_Q } from "../../constants";


class NewOpenQuestionForm extends React.Component {
    // Initial state of the form: empty, but is_hidden is set to false.
    state = {
        question_id: 0,
        question_text: "",
        is_hidden: false
    };

    // Preparations before the component appears on screen.
    componentDidMount() {
        // If the form receives a question prop, the question object is
        // passed to this (NewOpenQuestionForm) component. It then extracts the id and text from the question obj.
        // Then it sets the component's state using setState to update id and text.
        if (this.props.question) {
            const {
                question_id,
                question_text
            } = this.props.question;
            this.setState({
                question_id,
                question_text
            });
        }
    }

    // Handles the changes of the input element.
    // Takes input from the user and updates the state of the component
    // with the new value. (you fill in the form and your input will be the new state
    // of the form.)
    onChange = e => {
        this.setState({
            [e.target.name]: e.target.value
        });
    };

     // Handles the addition of new questions to the database.
     createOpenQuestion = (e) => {
        e.preventDefault();
        // Post new question to Question database with the given
        // user text input and visibility set in the state.
        axios.post(
            API_URL_OPEN_Q, this.state)
            // When POST is executed (when Toevoegen is clicked) the resetState method
            // from the OpenQuestions component will be executed, the form disappears from the screen,
            // and all questions will be fetched from the database.
            .then(() => {
                this.props.resetState();
                this.props.toggle();
                this.props.getOpenQuestions();
                this.refreshPage()
            });
     };

    editOpenQuestion = e => {
        e.preventDefault();
        axios.put(API_URL_OPEN_Q +
            this.state.question_id,
            this.state.question_text).then(() => {
                this.props.resetState();
                this.props.toggle();
                this.props.getOpenQuestions();
        });
    };

    refreshPage = () => {
        window.location.reload();
    }

    defaultIfEmpty = value => {
        return value === "" ? "" : value;
    };

    render() {
        return (
            <Form
                onSubmit={
                this.props.question
                    ? this.editOpenQuestion
                    : this.createOpenQuestion}>
                <FormGroup>
                    <Label for="question_text">Vraag:</Label>
                    <Input
                        type="text"
                        name="question_text"
                        onChange={this.onChange}
                        value={this.defaultIfEmpty(this.state.question_text)}
                        autoFocus
                        required
                        />
                </FormGroup>
                <Button
                    color="success"
                >Toevoegen</Button>
            </Form>
        );
    }
}

export default NewOpenQuestionForm;