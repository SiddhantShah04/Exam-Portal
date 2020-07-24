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

const action = async(examId) =>{
	
    let status = document.querySelector("#Active")

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
}

const del= async(examId,subject) => {
	
document.querySelector(`#del_${examId}`).remove()
	const response = await fetch("/delete",{
        method : 'POST',
		cache: 'no-cache',
		credentials:'include', 
        headers : {'Content-Type': 'application/json'},
        body:JSON.stringify({examId,subject})
    })
	const result = await response.text()
	if(result == "Deleted"){
		
		
	}
}