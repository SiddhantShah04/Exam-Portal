
let getQuestion =new Student(result,Roll)

document.addEventListener('DOMContentLoaded', function () {
    setQuestion()
    setInterval(DSeconds, 1000);
    });

// when we click on option
const optionClicked = (value)=>{
    
    getQuestion.setSelectedOption(value)
    setQuestion()
} 
// when we click on option button
const skip = ()=>{
    let r=confirm("Are you really wants to skip to next question?");
    if(r==true){
        setQuestion()
    }
}

// when we click on submit answer
const submitAnswers = ()=>{
    let r=confirm("Are you really wants to submit your answers and finish your exam?");
    if(r==true){
        getQuestion.endExam(Roll)
    }
}

const setQuestion = () => {
    if(getQuestion.totalQuestion()==getQuestion.getQuestionNo()+1 )
    {
        getQuestion.endExam(Roll)
        //sent a ajax requestion to submit answers
    }
    let question = getQuestion.getNextQuestion()
    if(question==false){
        return(0)
    }
    if(question[7]!= null){
        document.querySelector("#img").innerHTML = `<img src="/static/images/${question[7]}" style='width:500px;height:270px;'>`
    }
    else{
        document.querySelector("#img").innerHTML=null
    }
    
    document.querySelector(".q").innerHTML = question[2]
    document.querySelector("#Qno").innerHTML = getQuestion.getQuestionNo()+1+"/"+getQuestion.totalQuestion()
    document.getElementById("Time").innerHTML = question[8];
    document.querySelector("#options").innerHTML = '';
    let options=[question[3],question[4],question[5],question[6]]
    options.map(elt => {
        document.querySelector("#options").innerHTML += `<button value='${elt}' onclick='optionClicked(this.value)' class="option">${elt}</button>`
    })
    
}

function DSeconds(){
    var i = document.getElementById("Time").innerHTML;
    document.getElementById("Time").innerHTML=--i;
    
 if(i==0){
     setQuestion()
 }   
}
