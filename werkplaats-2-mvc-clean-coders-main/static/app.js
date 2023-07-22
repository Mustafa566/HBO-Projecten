function getQuestionInfo() {
    if (document.querySelector('.questions')) {

        const button = document.querySelectorAll('.btnModal')
        const template = document.querySelector('#getQuestionTemplate')
        const results = document.querySelector('.modal-body')
        button.forEach((item) => {
            item.addEventListener('click', (i) => {
                const rowId = item.childNodes[1].value
                axios.get('/getModalResults/' + rowId).then((response) => {
                    const data = response.data
                    results.innerHTML = ''
                    data.forEach((item) => {
                        var itemContent = template.innerHTML
                            .replace('@vraag', item[2])
                            .replace('@id', item[0])

                        results.innerHTML += itemContent
                    })

                }, (error) => {
                    console.log(error);
                })
            })

        })
    }
}

function editQuestion() {
    if (document.querySelector('.questions')) {
        const updateBtn = document.querySelector('.save_btn')

        updateBtn.addEventListener('click', (i) => {
            const rowId = document.querySelector('.modal-body .rowId').value
            const question = document.querySelector('.modal-body .vraag').value
            const select_learning = document.getElementById("select_learning");
            const learningobjectId = select_learning.options[select_learning.selectedIndex].value;
            const select_author = document.getElementById("select_author");
            const authorobjectId = select_author.options[select_author.selectedIndex].value;

            axios.post('/edithInfo/' + rowId + '/' + question + '/' + learningobjectId + '/' + authorobjectId).then((response) => {
                location.reload()
            }, (error) => {
                console.log(error);
            });
        })
    }
}

function getAuthorInfo() {
    if (document.querySelector('.author')) {

        const button = document.querySelectorAll('.btnModal')
        const template = document.querySelector('#getAuthorTemplate')
        const results = document.querySelector('.modal-body')
        button.forEach((item) => {
            item.addEventListener('click', (i) => {
                const rowId = item.childNodes[1].value
                axios.get('/getModalAuthorResults/' + rowId).then((response) => {
                    const data = response.data
                    results.innerHTML = ''
                    data.forEach((item) => {
                        var itemContent = template.innerHTML
                            .replace('@id', item[0])
                            .replace('@auteur', item[1])
                            .replace('@geboortejaar', item[3])
                            .replace('@medewerker', item[4])
                            .replace('@achternaam', item[2])
                            .replace('@metpensioen', item[5])


                        results.innerHTML += itemContent
                    })

                }, (error) => {
                    console.log(error);
                })
            })
        })
    }
}

function editAuthor() {
    if (document.querySelector('.author')) {
        const updateBtn = document.querySelector('.save_btn')

        updateBtn.addEventListener('click', (i) => {
            const voornaam = document.querySelector('.modal-body .auteur').value
            const achternaam = document.querySelector('.modal-body .achternaam').value
            const geboortejaar = document.querySelector('.modal-body .geboortejaar').value
            const medewerker = document.querySelector('.modal-body .medewerker').value
            const pensioen = document.querySelector('.modal-body .pensioen').value
            const rowId = document.querySelector('.modal-body .rowId').value

            axios.post('/editAuteurs/' + voornaam + '/' + achternaam + '/' + geboortejaar + '/' + medewerker + '/' + pensioen + '/' + rowId).then((response) => {
                location.reload()
            }, (error) => {
                console.log(error);
            });
        })
    }
}

function deleteQuestion() {
    if (document.querySelector('.questions')) {
        const btnDeleteForm = document.querySelectorAll('.btnDeleteForm')
        const deleteBtn = document.querySelector('.deleteBtn')
        btnDeleteForm.forEach((item) => {
            item.addEventListener('click', (i) => {
                const rowId = item.getAttribute('data-id')
                axios.delete('/deleteQuestion/' + rowId).then((response) => {
                    location.reload()
                }, (error) => {
                    console.log(error);
                });
            })
        })
    }
}

function searchFilter() {
    if (document.querySelector('.questions')) {
        const template = document.querySelector('#template')
        const orgResults = document.querySelector('#orgResults')
        const results = document.querySelector('#results')
        const clockLoader = document.querySelector('.clock-loader')
        const resultsSearch = document.querySelector('#resultsSearch')
        const answerButtonTd = document.querySelectorAll('#answerButtonTd')
        document.querySelector('.searchBar').addEventListener('keyup', function () {
            const textInput = this.value
            if (textInput != '') {

                orgResults.style.display = 'none'
                axios.get('/getResults/' + textInput).then((response) => {
                    const data = response.data
                    if (data.length != 0) {
                        resultsSearch.style.display = 'Block'
                        results.innerHTML = '';
                        data.forEach(function (item) {
                            answerButtonTd.innerHTML =
                                `
                        <form action="" method="GET" class="btnAnswer">
                            <input class="rowId" type="text" style="display: none" value="${item[0]}">
                            <button type="button" class="answerButton answer">
                                Antwoord
                            </button>
                        </form>
                        `;
                            var itemContent = template.innerHTML
                                .replaceAll('@id', item[0])
                                .replace('@leerdoel', item[1])
                                .replace('@vraag', item[2])
                                .replace('@auteur', item[3])
                                .replace('@antwoord', answerButtonTd.innerHTML)
                            results.innerHTML += itemContent
                        })
                        answerButton('.btnAnswer')
                    } else {
                        resultsSearch.style.display = 'None'
                    }
                }, (error) => {
                    console.log(error);
                });
            } else {
                resultsSearch.style.display = 'None'
                clockLoader.style.opacity = 1

                setTimeout(function () {
                    orgResults.style.display = 'Block'
                    clockLoader.style.opacity = 0
                }, 10);
            }
        })

        // Search on id
        document.querySelector('.searchBarId').addEventListener('keyup', function () {
            const textInput = this.value
            if (textInput != '') {
                orgResults.style.display = 'none';
                axios.get('/getResultsId/' + textInput).then((response) => {
                    const data = response.data
                    if (data.length != 0) {
                        resultsSearch.style.display = 'Block';
                        results.innerHTML = '';
                        data.forEach(function (item) {
                            answerButtonTd.innerHTML =
                                `
                        <form action="" method="GET" class="btnAnswer">
                            <input class="rowId" type="text" style="display: none" value="${item[0]}">
                            <button type="button" class="answerButton answer">
                                Antwoord
                            </button>
                        </form>
                        `;
                            var itemContent = template.innerHTML
                                .replace('@id', item[0])
                                .replace('@leerdoel', item[1])
                                .replace('@vraag', item[2])
                                .replace('@auteur', item[3])
                                .replace('@antwoord', answerButtonTd.innerHTML)
                            results.innerHTML += itemContent
                        })
                        answerButton('.btnAnswer')
                    } else {
                        resultsSearch.style.display = 'None'
                    }
                }, (error) => {
                    console.log(error);
                });
            } else {
                resultsSearch.style.display = 'None'
                clockLoader.style.opacity = 1

                setTimeout(function () {
                    orgResults.style.display = 'Block'
                    clockLoader.style.opacity = 0
                }, 10);
            }
        })
    }
}

function answerButton(className) {
    const button = document.querySelectorAll(className);
    var answerId = 0;
    button.forEach((item) => {
        item.addEventListener('click', (i) => {
            const rowId = item.childNodes[1].value
            axios.get('/getModalResults/' + rowId).then((response) => {
                const data = response.data
                data.forEach((getId) => {
                    answerId = getId[0]
                })
                window.open(`https://www.test-correct.nl/?vraag=${answerId}`, '_blank').focus();
            }, (error) => {
                console.log(error);
            })
        })
    })
}

function birthFilter() {
    if (document.querySelector('#authors')) {
        const filterBtn = document.querySelector('.btnFilter')
        const filterTemplate = document.querySelector('#filterTemplate')
        const orgResults = document.querySelector('#orgResults')
        const results = document.querySelector('#results')
        const filterSearch = document.querySelector('#filterSearch')
        const terugFilter = document.querySelector('.terugFilter')
        filterBtn.addEventListener('click', (i) => {
            axios.get('/birthFilter/').then((response) => {
                const data = response.data
                if (data.length != 0) {
                    orgResults.style.display = 'None'
                    filterSearch.style.display = 'Block'
                    results.innerHTML = '';
                    data.forEach(function (item) {
                        var itemContent = filterTemplate.innerHTML
                            .replaceAll('@id', item[0])
                            .replace('@voornaam', item[1])
                            .replace('@achternaam', item[2])
                            .replace('@geboortejaar', item[3])
                            .replace('@medewerker', item[4])
                            .replace('@met_pensioen', item[5])
                        results.innerHTML += itemContent
                    })
                }
            })

        })
        terugFilter.addEventListener('click', (i) => {
            filterSearch.style.display = 'None'
            orgResults.style.display = 'Block'
        })
    }

}

function addQuestion() {
    if (document.querySelector('.questions')) {
        const createBtn = document.querySelector('.create_btn')

        createBtn.addEventListener('click', (i) => {
            let question = document.querySelector('.modal-body .vraag').value;
            let learningobjectId = document.querySelector('.modal-body .leerdoel').value;
            let authorobjectId = document.querySelector('.modal-body .auteur').value;
            axios.post('/addQuestion/' + question + '/' + learningobjectId + '/' + authorobjectId).then((response) => {
                location.reload()
            }, (error) => {
            });
        })
    }
}

function showMore() {
    const template = document.querySelector('#template')
    const orgResults = document.querySelector('#orgResults')
    const results = document.querySelector('#results')
    const clockLoader = document.querySelector('.clock-loader')
    const answerButtonTd = document.querySelectorAll('#answerButtonTd')
    const resultsSearch = document.querySelector('#resultsSearch')
    let showMoreBtns = document.querySelectorAll('.showMoreBtn');
    showMoreBtnValue = 10

    showMoreBtns.forEach((showMoreBtn) => {
        showMoreBtn.addEventListener('click', (i) => {
            showMoreBtnValue = showMoreBtnValue + 50
            axios.get('/showMoreResults/' + showMoreBtnValue).then((response) => {
                const data = response.data
                orgResults.style.display = "None"
                if (data.length != 0) {
                    resultsSearch.style.display = 'Block'
                    results.innerHTML = '';
                    data.forEach(function (item) {
                        answerButtonTd.innerHTML =
                            `
                        <form action="" method="GET" class="btnAnswer">
                            <input class="rowId" type="text" style="display: none" value="${item[0]}">
                            <button type="button" class="answerButton answer">
                                Antwoord
                            </button>
                        </form>
                        `;
                        var itemContent = template.innerHTML
                            .replaceAll('@id', item[0])
                            .replace('@leerdoel', item[1])
                            .replace('@vraag', item[2])
                            .replace('@auteur', item[3])
                            .replace('@antwoord', answerButtonTd.innerHTML)
                        results.innerHTML += itemContent
                    })
                    answerButton('.btnAnswer')
                } else {
                    resultsSearch.style.display = 'None'
                }
            }, (error) => {
                console.log(error);
            });
        })
    })
}


function deleteAuthor() {
    if (document.querySelector('.author')) {
        const btnDeleteForm = document.querySelectorAll('.btnDeleteForm')
        btnDeleteForm.forEach((item) => {
            item.addEventListener('click', (i) => {
                const rowId = item.getAttribute('data-id')
                if (confirm("wilt u de auteur verwijderen?") == true) {
                    axios.delete('/deleteAuthor/' + rowId).then((response) => {
                        location.reload()
                    }, (error) => {
                        console.log(error);
                    });

                }

            })
        })
    }
}

deleteAuthor()

getQuestionInfo()
editQuestion()
searchFilter()
answerButton('.btnAnswer')
birthFilter()
deleteQuestion()
addQuestion()
showMore()
editAuthor()
getAuthorInfo()

