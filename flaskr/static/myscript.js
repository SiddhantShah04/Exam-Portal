window.onload = () => {
    // Get a modal
    let modal = document.querySelector("#myModal");
    // Get the button that opens the modal
    let btnModal = document.querySelector("#signup");
    // On button click open the modal for signup
    btnModal.onclick = () => {
        modal.style.display = 'block'
    }
// When user click om anywhere on the screen close the modal
    window.onclick  = () => {
        if(event.target == "modal"){modal.style.display='none'}
    }
    document.querySelector(".close").onclick = ()=>{modal.style.display = 'none'}
}

const restrationForm = async() => {
    document.querySelector("#error").innerHTML ="Creating your account.......";
    let username = document.querySelector("#username").value
    let password = document.querySelector("#password").value
    // now just send a ajax request to auth.register
    const response = await fetch("/auth/register",{
        method : 'POST',
		cache: 'no-cache',
		credentials:'include', 
        headers : {'Content-Type': 'application/json'},
        body:JSON.stringify({username,password})
    })
    // what ever  error is sent it to label error
    document.querySelector("#username").value = null
    document.querySelector("#password").value = null
    const result = await response.text()
    document.querySelector("#error").innerHTML = result; 
}

const semSelect = (value) => {
    let selectedSubject = document.querySelector("#Subject")
    selectedSubject.innerHTML = null
        let sem = {
            2:["Programming with C","Programming with Python 2","Linux","Data Structures","Calculus","Statistical Methods and Testing of Hypothesis","Green Technologies"],
            3:["Operating Systems","Web Programming","Core Java","Database Management Systems",
            "Combinatorics and Graph Theory","Linux","Calculus"],
            4:["Software Engineering","Advanced JAVA","Computer Networks","Android Developer Fundamentals","Fundamentals of Algorithms  ",
            "Dot Net Technologies","Linear Algebra using Python "],
            5:["Artificial Intelligence","Linux System Administration","Information and Network Security"," Linux System Administration",
            "Architecting of IoT","Game Programming","Game Programming"],
            6:["Wireless Sensor Networks and Mobile Communication","Cloud Computing ","Digital Image Processing",
            "Data Science","Ethical Hacking","Cyber Forensics","Information Retrieval"]
        }
        sem[value].map((elt) => {
        // Learning thing here is always put "" in value,fuck wasted 1 hour on this stupid bug..
        selectedSubject.innerHTML+=`<option value="${elt}"></option>`})
}
const qPaperSubmit = async() =>{
    let error = document.querySelector("#error")
    error.innerHTML = "Uploading your questions"
    // Get the branch.
    let select = document.querySelector(".branch")
    const branch = select.options[select.selectedIndex].value
    
    // Select the semester.
    select  = document.querySelector(".sem")
    const sem = select.options[select.selectedIndex].value
    
    // Select the subject
    const subject  = document.querySelector(".subject").value
    
    // Csv question containing file
    const file = document.querySelector(".file").value

    const response = await fetch("/uploadQuestion",{
        method : 'POST',
		cache: 'no-cache',
		credentials:'include', 
        body:file,
    })
    const result = await response.text()

}














