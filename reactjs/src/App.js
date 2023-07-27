import React,{useState, useEffect} from "react";
import './App.css'
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
                    <div className="sas">

                    <div className="sa">
                        {course.symbol}
                    </div>
                     
                        {(course.condition==='up')?(
  
                        <div className="sa as bg-success">
                        {course.price}
                      </div>):(<div className="sa as bg-danger">
                        {course.price}
                      </div>)}
                    
                    

                    </div>
            
          ))
        )}
    </div>
  );
}

export default App;
