import React,{useState, useEffect} from "react";


function App() {

  const [data,setData]=useState([{}])
  useEffect(()=>{
    fetch('http://localhost:5000/v1/courses').then(res=>res.json()).then(data=>{
      setData(data)
      console.log(data)
    })
  },[])

  return (
    <div>
        {(typeof data.courses==='undefined')?(<p>Loading ... </p>):(
          data.courses.map((course,i)=>(
            
            <table border={1} className="sa">
              <thead>
                <tr>
                  <th>symbol</th>
                  <th>price</th>
                </tr>
              </thead>
              <tbody key={i}>
                  <td width={250} align="center">{course.symbol}</td>
                  <td width={250} align="center"> {course.price} </td>

              </tbody>
            
            </table>

            
            
          ))
        )}
    </div>
  );
}

export default App;
