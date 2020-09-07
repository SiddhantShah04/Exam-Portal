class Student {
    constructor(question,Roll){
        this.question =[]
        if(localStorage.getItem('roll') != null && localStorage.getItem('roll')==Roll ){
            this.answer =  JSON.parse(localStorage.getItem('answer'))
            question = JSON.parse(localStorage.getItem('question')) 
            question.map(elt => this.question.push(elt))
            this.questionNo = parseInt(localStorage.getItem('questionNo'))-1    
        }else{
            localStorage.clear();
            localStorage.setItem('roll',Roll)
            this.answer = {}
            this.questionNo = -1
            question.map(elt => this.question.push(elt))
            localStorage.setItem("question",JSON.stringify(question))
        }
    }

    // Return total number of questions in array
    totalQuestion(){
        return(this.question.length)
    }

    // Return the question Number
    getQuestionNo(){
        return(this.questionNo)
    }

    //Timer
    timer(){
    let i = document.querySelector(".countdown").innerHTML;

        document.querySelector(".countdown").innerHTML=--i;
        if(i==0){
            window.location.replace("/");
        }
    }

    // End the exam of student
    async endExam(Roll){
        let answer = this.answer
        let subject = this.question[0][1]
        
        const response = await fetch("/student/submitAnswer",{
            method : 'POST',
            cache: 'no-cache',
            credentials:'include', 
            headers : {'Content-Type': 'application/json'},
            body:JSON.stringify({Roll,answer,subject})
        })
        const result = await response.json()
        // Get a modal
        let modal = document.querySelector("#myLoggedModal");
        modal.style.display = 'block'
        if(result == "s"){
            //document.write("Your exam has been completed and result has been submitted to the server of our college.")
            document.querySelector("#sucess").style.display = 'block'
            document.querySelector("#failed").style.display = 'none'
            setInterval(this.timer, 1000);
        }else{
            document.querySelector("#failed").style.display = 'block'    
        }
        return(result)
    }
    
    // Set the selected option click by students
    setSelectedOption(selectedOption){
        let questionId = this.question[this.questionNo][0]
        
        this.answer[questionId]=selectedOption
        localStorage.setItem('answer',JSON.stringify(this.answer))
    }

    // Return the next question,take selected option and question id as argument
    getNextQuestion(){
        if(this.questionNo>=0 && (document.getElementById("Time").innerHTML > this.question[this.questionNo][8]-5)){
        console.log(this.question[this.questionNo][8]-5)

            return(false)
        }
        this.questionNo += 1
        localStorage.setItem('questionNo',this.questionNo)         
        return(this.question[this.questionNo])
    }
}
