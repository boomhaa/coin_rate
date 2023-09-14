import React,{useState, useEffect} from "react";
import {Link} from 'react-router-dom'
import '../App.css'
import axios from "axios";

export const MainPage = () => {
    const [data,setData]=useState([{}])
    const [user, setUser] = useState({});
    const [error,setError]=useState()
    const logoutUser =()=>{
      axios.post('http://127.0.0.1:5000/logout',{},{
        withCredentials: true,
      });
      window.location.href='/about';
  
    }
    
    useEffect(()=>{
      fetch('http://localhost:5000/v1/courses').then(res=>res.json()).then(data=>{
        setData(data)
        console.log(data)
      })
    },[])
    useEffect(()=>{
      axios.get('http://127.0.0.1:5000/me',{
          withCredentials: true,
        }).then((response)=>{setUser(response.data); console.log(response)}).catch(function(error){
        console.log(error,error.response.status)
        setError(error.response.status)
      })},[])
    
    const [value,setValue]=useState('')
    const filteredCoins=data.courses && data.courses.filter(coin=>{
      return coin.symbol.toLowerCase().includes(value.toLowerCase())
    })

    const [CheckBox,setCheckBox]=useState([])
    function handleChange(e){

if (e.target.value){
  setCheckBox([...CheckBox,e.target.value]);

}else{
  setCheckBox(CheckBox.filter((item)=>item!==e.target.value));
}

    }
    const FavoriteRates=()=>{
      axios.post('http://127.0.0.1:5000/favorite_rates',{favorite_rates:CheckBox},{withCredentials:true})
      window.location.href = '/'
    }

    return (
      <div >
        {Object.keys(user)==0 ? (<div>
        <h1>
        <Link to='/login'> login</Link>
        </h1>
        <p>
          Or <Link to='/register'> register</Link>
        </p>

        
        </div>):(<div>
          <p>Logged in</p>
          <p>ID: {user.id}</p>
          <p>Email: {user.email}</p>
          <button onClick={logoutUser}>Logout</button>
          <p>page <Link to='/about'>about me</Link></p>
        </div>)}
        <div className="form-center">
        <input
        type="text"
        placeholder="Search"
        
        onChange={(event)=>setValue(event.target.value)}
      />
      </div>
      <br/>
          {(typeof data.courses==='undefined')?(<p>Loading ... </p>):((Object.keys(user)==0)?((filteredCoins.length===0)?(<p className="form-center">There are no such courses
          </p>):(<div><p>You need to login on for choosing a favorite rates</p>
            {filteredCoins.map((course,i)=>(
              
                
                      <div className="sas1">
                      <div className="sa">
                          {course.symbol}
                      </div>
                          {(course.condition==='up')?(
                          <div className="sa as bg-success bg-opacity-75">
                          {course.price}
                        </div>):(<div className="sa as bg-danger bg-opacity-75">
                          {course.price}
                        </div>)}
                      </div>))

}</div>)
                          ):((filteredCoins.length===0)?(<p className="form-center">There are no such courses</p>):(<div>{(CheckBox.length===0)?(<div><p className="saw">You didn't choose favorite rates</p>
                          </div>):(<div><p>Your favourite rates are {CheckBox.join(', ')}</p> <button onClick={FavoriteRates}>Save</button></div>)}{filteredCoins.map((course,i)=>(

                
<div className="sas">
<input value = {course.symbol} type = "checkbox" onChange = {handleChange} />
<div className="sa">
    {course.symbol}
</div>
    {(course.condition==='up')?(
    <div className="sa as bg-success bg-opacity-75">
    {course.price}
  </div>):(<div className="sa as bg-danger bg-opacity-75">
    {course.price}
  </div>)}
</div>
))}</div>
            
                          )))}
      </div>
    );
}