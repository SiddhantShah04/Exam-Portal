window.onload = () => {
    activeSubject();
    const r = setInterval(activeSubject,10000)

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

// When DOM window is loaded call the activeSubject() to get active subjects

const activeSubject = async() => {
    const response = await fetch("/getSubject",{
    })
    const result = await response.json()   
    let addSubject  = document.querySelector("#addActiveSubject")
    addSubject.innerHTML=''
        result.map((elt)=>{
            addSubject.innerHTML += `<option>${elt}</option>`
        })
}

const checkStudent = async() => {
    let x = document.querySelector("#addActiveSubject")
    let Selectedsubject = x.options[x.selectedIndex].text
    let rollNumber = document.querySelector("#roll").value
    
    const response = await fetch("/studentLogin",{
        method : 'POST',
		cache: 'no-cache',
		credentials:'include', 
        headers : {'Content-Type': 'application/json'},
        body:JSON.stringify({Selectedsubject,rollNumber})
    })
    
    const result = await response.text()
    let studentPaper = document.querySelector("#studentPaper")
    if(result != "ok"){
        if(rollNumber==localStorage.getItem("roll")){
            studentPaper.submit()
        }else{
            document.querySelector("#errorStudent").innerHTML = result; 
        }
    }else{
        localStorage.clear();
        studentPaper.submit()
    }

}

const studentLogin = () => {
    
    checkStudent()
    
    return(false)
}


    













