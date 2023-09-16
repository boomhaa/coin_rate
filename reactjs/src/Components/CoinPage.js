import React,{useEffect, useState} from "react";
import { useLocation } from "react-router-dom";
import Chart from "chart.js/auto"; // Importing the Chart.js library
import { Line } from "react-chartjs-2";

export const CoinPage =()=>{
    const location=useLocation();
    const [data,setData]=useState([])
    useEffect(()=>{
      fetch('http://localhost:5000/v1/courses'+location.pathname).then(res=>res.json()).then(data=>{
        setData(data)
        console.log(data)
      })
    },[])
    
    const labels=[];
    let i=200;
while (i>=0){
  labels.push(i);
  i-=10;
}
// Setting up the data for the chart, including the labels and datasets
const data_for_graphic = {
  labels:labels,
  datasets: [
    {
      label: "My First dataset", // Setting up the label for the dataset
      backgroundColor: "rgb(255, 99, 132)", // Setting up the background color for the dataset
      borderColor: "rgb(255, 99, 132)", // Setting up the border color for the dataset
      data: data[0]&&data[0].history,
      
     // Setting up the data for the dataset
    },
  ],
};
    return(
        <div>

{(typeof data==='undefined')?(<p>Loading ... </p>):(<div>{data.map((course,i)=>(
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

            ))}<div className="canvas-container">
              
            <Line data={data_for_graphic}/>
            </div></div>
          )}

        </div>
    )


}