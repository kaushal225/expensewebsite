const searchField=document.querySelector('#searchField');
const tbody=document.querySelector('.table-body')
const paginationContainer=document.querySelector('.pagination-container')

const appTable=document.querySelector('.app-table');

const tableOutput =document.querySelector('.table-output');
tableOutput.style.display='none';

searchField.addEventListener('keyup',(e)=>{
    const searchValue = e.target.value;
    if(searchValue.length>0){
        tbody.innerHTML='';
        paginationContainer.style.display='none';

        fetch("/search-expenses",{
            body:JSON.stringify({searchText:searchValue}),
            method:"POST",
        }).then(res => res.json()).then(data => {
            console.log('here')
            appTable.style.display='none';
            tableOutput.style.display='block';
               if(data.length===0){
                   tbody.innerHTML='no result found';
               }
               else{

                data.forEach(element => {
                    tbody.innerHTML+=  `
                    <tr>
                    <td> ${element.amount} </td>
                    <td> ${element.category} </td>
                    <td> ${element.description} </td>
                    <td> ${element.date}  </td>
                    </tr>
                    
                    `;
                });
                 
                 
               }

        });
    }
    else{
        appTable.style.display='block';
        paginationContainer.style.display='block';
        tableOutput.style.display='none';

      }


});