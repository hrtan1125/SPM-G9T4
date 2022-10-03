import { useGlobalContext } from '../context'

const ShowSkills = () => {
<<<<<<< Updated upstream
  const { selectedMeal, closeModal } = useGlobalContext()

=======
  const { selectedMeal, closeModal, role } = useGlobalContext()

  console.log("cuterole", role)
>>>>>>> Stashed changes
  return <aside className='modal-overlay'>
    <div className='modal-container'>
      {/* <img src={image} className="img modal-img" />
      <div className='modal-content'>
        <h4>{title}</h4>
        <p>Cooking Instructions</p>
        <p> {text}</p>
        <a href={source} target="_blank">Original Source</a>
        <button className="btn btn-hipster close-btn" onClick={closeModal}>close</button>
      </div> */}
    </div>
  </aside>
}

export default ShowSkills