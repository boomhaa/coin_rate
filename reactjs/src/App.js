import {MainPage} from './Components/MainPage';
/*global event*//*eslint no-restricted-globals: ["error", "event"]*/import {CoinPage} from './Components/CoinPage';
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

<Route path='/' element={<MainPage/>} />
<Route path={location.pathname} element={<CoinPage/>}/>


  </Routes>
  
  </BrowserRouter>
)
 
}

export default App;
