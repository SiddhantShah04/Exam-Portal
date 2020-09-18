
let getQuestion =new Student(result,Roll)

document.addEventListener('DOMContentLoaded', function () {
    setQuestion()
    setInterval(DSeconds, 1000);
    });


const optionClicked = (value)=>{
    
    getQuestion.setSelectedOption(value)
    setQuestion()
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
    document.querySelector(".options").innerHTML = '';
    let options=[question[3],question[4],question[5],question[6]]
    options.map(elt => {
        document.querySelector(".options").innerHTML += `<button value='${elt}' onclick='optionClicked(this.value)' class="option">${elt}</button>`
    })
    
}

function DSeconds(){
    var i = document.getElementById("Time").innerHTML;
    document.getElementById("Time").innerHTML=--i;
    
 if(i==0){
     setQuestion()
 }   
}
