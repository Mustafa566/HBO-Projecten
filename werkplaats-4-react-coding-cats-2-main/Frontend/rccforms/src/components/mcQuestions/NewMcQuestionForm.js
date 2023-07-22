// Code inspired by
// https://blog.logrocket.com/using-react-django-create-app-tutorial/

import React from "react";
import { Button, Form, FormGroup, Input, Label } from "reactstrap";
import axios from "axios";
import { API_URL_MC_Q } from "../../constants";


class NewMcQuestionForm extends React.Component {
    // Initial state of the form: empty, but is_hidden is set to false.
    state = {
        mc_id: 0,
        question_text: "",
        option_a: "",
        option_b: "",
        option_c: "",
        option_d: "",
        is_hidden: false
    };

    // Preparations before the component appears on screen.
    componentDidMount() {
        // If the form receives a question prop, the question object is
        // passed to this (NewMcQuestionForm) component. It then extracts the id and text from the question obj.
        // Then it sets the component's state using setState to update id and text.
        if (this.props.question) {
            const {
                question_id,
                question_text,
                option_a,
                option_b,
                option_c,
                option_d
            } = this.props.question;
            this.setState({
                question_id,
                question_text,
                option_a,
                option_b,
                option_c,
                option_d
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
    createMcQuestion = (e) => {
        e.preventDefault();
        // Post new question to Question database with the given
        // user text input and visibility set in the state.
        axios
            .post(
            API_URL_MC_Q, this.state)
            // When POST is executed (when Toevoegen is clicked) the resetState method
            // from the McQuestions component will be executed, the form disappears from the screen,
            // and all questions will be fetched from the database.
            .then(() => {
                this.props.resetState();
                this.props.toggle();
                this.props.getMcQuestions();
                this.refreshPage();
            });
    };

    editMcQuestion = (e) => {
        e.preventDefault();
        axios.put(API_URL_MC_Q +
            this.state.question_id,
            this.state).then(() => {
                this.props.resetState();
                this.props.toggle();
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
                    ? this.editMcQuestion
                    : this.createMcQuestion}>
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
                <FormGroup>
                    <Label
                        for="optionA"
                    >
                        Optie A:
                    </Label>
                    <Input
                        type="text"
                        name="option_a"
                        onChange={this.onChange}
                        value={this.defaultIfEmpty(this.state.option_a)}
                        required
                        />
                </FormGroup>
                <FormGroup>
                    <Label
                        for="option_b"
                        >
                        Optie B:
                    </Label>
                    <Input
                        type="text"
                        name="option_b"
                        onChange={this.onChange}
                        value={this.defaultIfEmpty(this.state.option_b)}
                        required
                        />
                </FormGroup>
                <FormGroup>
                    <Label
                        for="option_c"
                        >
                        Optie C:
                    </Label>
                    <Input
                        type="text"
                        name="option_c"
                        onChange={this.onChange}
                        value={this.defaultIfEmpty(this.state.option_c)}
                        placeholder="Optioneel"
                        />
                </FormGroup>
                <FormGroup>
                    <Label
                        for="option_d"
                        >
                        Optie D:
                    </Label>
                    <Input
                        type="text"
                        name="option_d"
                        onChange={this.onChange}
                        value={this.defaultIfEmpty(this.state.option_d)}
                        placeholder="Optioneel"
                        />
                </FormGroup>
                <Button
                    color="success"
                >Toevoegen</Button>
            </Form>
        );
    }
}

export default NewMcQuestionForm;