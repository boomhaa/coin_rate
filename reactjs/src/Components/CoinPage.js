import React,{useEffect, useState} from "react";
import { useLocation } from "react-router-dom";

export const CoinPage =()=>{
    const location=useLocation();
    const [data,setData]=useState()
    useEffect(()=>{
      fetch('http://localhost:5000/v1/courses'+location.pathname).then(res=>res.json()).then(data=>{
        setData(data)
        console.log(data)
      })
    },[])
    return(
        <div>

{(typeof data==='undefined')?(<p>Loading ... </p>):(
            data.map((course,i)=>(
                      <div className="sas1">

                      <div className="sa">
                          {course.symbol}
                      </div>

                          {(course.condition==='up')?(

                          <div className="sa as bg-success bg-opacity-75" >
                          {course.price}
                        </div>):(<div className="sa as bg-danger bg-opacity-75">
                          {course.price}
                        </div>)}
                        
                        

                      </div>

            ))
          )}

        </div>
    )


}