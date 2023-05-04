const username_field=document.querySelector('#usernamefield');
const email_field=document.querySelector('#emailfield')

const show_password_toggle=document.getElementsByClassName('show-password-toggle')
const passwordfield=document.getElementsByClassName('passwordfield');

const feed_back_area=document.querySelector('.invalid-feedback')
const email_feed_back_area=document.querySelector('.email-feedback-area')
const usernameSuccessOutput=document.querySelector('.usernameSuccessOutput')
const submit_btn=document.querySelector('.submit-btn');

console.log(show_password_toggle);


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


const handle_toggle_input = (e) => {
   if(e.target.textContent==='SHOW'){
    e.target.textContent='HIDE';
    console.log(e.target)
    console.log(passwordfield)
    Array.from(passwordfield).forEach( e => e.setAttribute("type","text"));
   }
   else{
    e.target.textContent='SHOW';
    Array.from(passwordfield).forEach( e => e.setAttribute("type","password"));
   }


};

Array.from(show_password_toggle).forEach(element => {
    console.log('hek')
    console.log(element)
    element.addEventListener('click',handle_toggle_input)});


email_field.addEventListener('keyup',(e)=>{
    const email_val=e.target.value;
    if(email_val.length>0){
    fetch("/authentication/validate-email",{
        body:JSON.stringify({email:email_val}),
        method:"POST",
    }).then(res => res.json()).then(data => {
        if(data.email_error){
            submit_btn.setAttribute("disabled","disabled");
            email_field.classList.add('is-invalid');
            email_feed_back_area.style.display='block';
            email_feed_back_area.innerHTML= `<p> ${data.email_error} </p>`
        }
        else{
            submit_btn.removeAttribute("disabled");
            email_field.classList.remove('is-invalid');
            email_feed_back_area.style.display='none';
        }
    });
  }
});











username_field.addEventListener('keyup',(e) => {
    //console.log(e);
    const username_val=e.target.value;
    usernameSuccessOutput.style.display='block';
    usernameSuccessOutput.textContent=`checking ${username_val}`;
    if(username_val.length>0){

    fetch("/authentication/validate-username",{
        body:JSON.stringify({username:username_val}),
        method:"POST",
    }).then(res => res.json()).then(data => {
        usernameSuccessOutput.style.display='none';
        if(data.username_error){
            submit_btn.setAttribute("disabled","disabled");
            username_field.classList.add('is-invalid');
            feed_back_area.style.display='block';
            feed_back_area.innerHTML= `<p> ${data.username_error} </p>`
        }
        
        else{
            submit_btn.removeAttribute("disabled");
            username_field.classList.remove('is-invalid');
            feed_back_area.style.display='none';
        }
    });
  }
  else{
    usernameSuccessOutput.style.display='none';

  }
});