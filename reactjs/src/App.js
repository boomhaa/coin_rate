import {MainPage} from './Components/MainPage';
/*global event*//*eslint no-restricted-globals: ["error", "event"]*/import {CoinPage} from './Components/CoinPage';
import {LoginPage} from './Components/LoginPage';
import {RegisterPage} from './Components/RegisterPage';
import {LandingPage} from './Components/about_user';
import {
  useLocation,
  BrowserRouter,
  Routes,
  Route,
} from 'react-router-dom';
function App() {
  
return(
  <BrowserRouter>
  
  <Routes>
  <Route path='/about' element={<LandingPage/>}/>
<Route path='/' element={<MainPage/>} />
<Route path='/login' element={<LoginPage/>} />
<Route path='/register' element={<RegisterPage/>}/>

<Route path={location.pathname} element={<CoinPage/>}/>



  </Routes>
  
  </BrowserRouter>
)
 
}

export default App;
