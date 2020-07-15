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




