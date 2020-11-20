
const semSelect = (value) => {
let selectedSubject = document.querySelector("#Subject")
selectedSubject.innerHTML = null
        let sem = {
            2:["Programming with C","Programming with Python 2","Linux","Data Structures","Calculus","Statistical Methods and Testing of Hypothesis","Green Technologies"],
            3:["Operating Systems","Web Programming","Core Java","Database Management Systems",
            "Combinatorics and Graph Theory","Linux","Calculus"],
            4:["Software Engineering","Advanced JAVA","Computer Networks","Android Developer Fundamentals","Fundamentals of Algorithms  ",
            "Dot Net Technologies","Linear Algebra using Python "],
            5:["Artificial Intelligence","Linux System Administration","Information and Network Security",
            "Architecting of IoT","Game Programming"],
            6:["Wireless Sensor Networks and Mobile Communication","Cloud Computing ","Digital Image Processing",
            "Data Science","Ethical Hacking","Cyber Forensics","Information Retrieval"]
        }
        sem[value].map((elt) => {
        // Learning thing here is always put "" in value,fuck wasted 1 hour on this stupid bug..
        selectedSubject.innerHTML+=`<option value="${elt}"></option>`})
}

const action = async(examId, subject) =>{
	let modal = document.querySelector("#activeExam")
    modal.style.display='block'
    document.querySelector(".ic").onclick = ()=>{modal.style.display = 'none'}
    const subjectName = document.querySelector("#asubjectName").innerHTML = subject
    let activeExamTable =  document.querySelector("#activeExamTable")
    const response = await fetch("/getPaperData",{
        method : 'POST',
		cache: 'no-cache',
		credentials:'include', 
        headers : {'Content-Type': 'application/json'},
        body:JSON.stringify({subject})
    })
	const result = await response.json()
    console.log(result)
    
    result.map((elt)=>{
        var row = activeExamTable.insertRow();
        row.style.border = '1px solid #dddddd';
       
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        cell1.style.padding = '8px';
        cell1.innerHTML = `<td >${elt[0]}</td> `
        cell2.innerHTML = `<input type="text"  style="margin:2%;width:10%;line-height:25%;" />/${elt[1]}`;
    })
    /*
    let status = document.querySelector(`#Active_${examId}`)

    const response = await fetch("/status",{
        method : 'POST',
		cache: 'no-cache',
		credentials:'include', 
        headers : {'Content-Type': 'application/json'},
        body:JSON.stringify({examId})
    })
	const result = await response.text()
	
	if(result == "Active"){
		status.innerHTML = "Active"
		
		status.style.backgroundColor = "green"
	}else{
		status.innerHTML = "Deactive"
		status.style.backgroundColor = "red"
    }
    */	
}

const createPaper = ()=>{
    alert("sidd")
}

const del = async(examId,subject) => {
	
	const response = await fetch("/delete",{
        method : 'POST',
		cache: 'no-cache',
		credentials:'include', 
        headers : {'Content-Type': 'application/json'},
        body:JSON.stringify({examId,subject})
    })
	const result = await response.text()
	if(result == "Deleted"){
		document.querySelector(`#del_${examId}`).remove()
	}else{
        alert("This subject exam are still going on,please remove live students from logged")
    }
}

const logged = async(examId,subject) => {
    let modal = document.querySelector("#myLoggedModal")
    modal.style.display = 'block'
    document.querySelector(".iclose").onclick = ()=>{modal.style.display = 'none'}
    const subjectName = document.querySelector("#isubjectName").innerHTML = subject
    let loggedTable =  document.querySelector("#loggedTable")
    let rowCount =  loggedTable.rows.length
    for (var i = rowCount - 1; i > 0; i--) {
        loggedTable.deleteRow(i);
    }
       
        const response = await fetch("/logged",{
            method : 'POST',
            cache: 'no-cache',
            credentials:'include', 
            headers : {'Content-Type': 'application/json'},
            body:JSON.stringify({examId,subject})
        })
        const result = await response.json()

        result.map((elt)=>{
            var row = loggedTable.insertRow();
            row.style.border = '1px solid #dddddd';
            row.id = `del_${elt[0]}`
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            cell1.style.padding = '8px';
            cell1.className="loggedTd"
            cell2.className="loggedTd"
        cell1.innerHTML = `<label  >${elt[2]} </label> `
        cell2.innerHTML = `<a onclick=removeStudent(${elt[0]}) style="cursor: pointer;padding-top:0.7%;color:red"><u>Retake</u></a>`
        
       })

    
}
const removeStudent  = async(id)=>{
    
    const response = await fetch("/removeStudent",{
        method : 'POST',
		cache: 'no-cache',
		credentials:'include', 
        headers : {'Content-Type': 'application/json'},
        body:JSON.stringify({id})
    })
    const result = await response.text()
    
    if(result=="Done"){document.querySelector(`#del_${id}`).remove()}
}
const editpaper = async(examId,subject)=>{
    let modal = document.querySelector("#myModal")

    modal.style.display='block'
    let editTable =  document.querySelector("#editQuestion")
    document.querySelector(".close").onclick = ()=>{modal.style.display = 'none'}
    
    if(editTable.rows.length==1){

        const subjectName=document.querySelector("#subjectName").innerHTML = subject
        const response = await fetch("/editPaper",{
            method : 'POST',
		    cache: 'no-cache',
		    credentials:'include', 
            headers : {'Content-Type': 'application/json'},
            body:JSON.stringify({examId,subject})
        })
	    const result = await response.json()
    
        result.map((elt)=>{
            var row = editTable.insertRow();
            row.style.border = '1px solid #dddddd';
            row.id = `del_${elt[0]}`
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            cell1.style.padding = '8px';
            cell1.innerHTML = `<td >${elt[3]} </td> `
            cell2.innerHTML = `<input type = "file" name = "file" class="file_${elt[0]}" style="margin:2%" />
            <button onclick = 'uploadImage(${elt[0]})' style="margin:2%;">Submit</button>`;
        })
    }
}

const uploadImage = async(id)=>{
    console.log(id)
    let photo = document.querySelector(".file_"+id).files[0];
    
    if(photo == null){
        alert("Choose a proper image")
         return(false)
        }   
    let formData = new FormData();
    formData.append("photo", photo);
    
    
    const response = await fetch("/uploadImage?id="+id,{
        method : 'POST',
		contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false,
        body:formData
    })
    const result = await response.json()
    console.log(result)
    if(result=="Saved"){document.querySelector(`#del_${id}`).remove()}
    
    }
