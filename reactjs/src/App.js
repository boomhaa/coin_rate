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
            <p key={i}>price={course.price} symbol={course.symbol} </p>
          ))
        )}
    </div>
  );
}

export default App;
