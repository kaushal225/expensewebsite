custom_toggle_button=document.getElementById('custom-toggle-button');
/* console.log(custom_toggle_button); */
custom_toggle_navbar=document.getElementById('custom-navbar-toggle');
custom_toggle_content=document.getElementById('custom-content-toggle');
notification_bell_icon=document.getElementById('notification-bell-icon');
body=document.getElementsByTagName('body')
console.log(notification_bell_icon)
/* console.log(custom_toggle_navbar);
console.log(custom_toggle_content); */

custom_toggle_button.addEventListener('click',(e)=>{
  custom_toggle_navbar.classList.toggle('hide-content');
  custom_toggle_content.classList.toggle('hide-content');
});

try{
member_input=document.getElementById('member-input')
member_select=document.getElementById('member-select')

member_input.addEventListener('keyup',(e)=>{
    member_select.innerHTML='';
    fetch('/groups/member_list',{
      method:'POST',
      body:JSON.stringify({searchText:e.target.value})
    }).then((data)=>data.json()).then((members=>{
      console.log(members);
        members.forEach(element => {
          console.log('ello');
          
            member_select.innerHTML+=   `
                <option name='member_name' value = ${element}>  ${element}  </option>
            
                `;       
        });
         
    })
     )
});
}catch(e){
  console.error(e);
}



group_name=document.getElementById('group_name');
join_group=document.getElementById('join_group');

console.log(join_group);

group_name.addEventListener('keyup',(e)=>{
  console.log(999);
  join_group.innerHTML='';
  fetch('/groups/join_group',{
    method:'POST',
    body:JSON.stringify({searchText:e.target.value})
  }).then((data)=>data.json()).then((element)=>{
       console.log(67)
       element.forEach(group => {
            join_group.innerHTML+=`<option name='group_name' value=${group} > ${group} </option>
            
            `;
       });
  });
});

 function change_bell_icon_color(){
 /*  prefentries=performance.getEntriesByType("back_forward");
  console.log('hello',prefentries); */
  fetch('/groups/list_notification',{
    method:'POST'
  }).then((data)=>data.json()).then((notification)=>{
    if(notification.notifications===true){
      notification_bell_icon.style.display="block";
    }
    else {
      notification_bell_icon.style.display="none";

    }
  });

}

//body.addEventListener("load",change_bell_icon_color(e.target));