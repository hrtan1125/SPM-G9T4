import * as React from 'react';
import Box from '@mui/material/Box';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { useGlobalContext } from '../context';

const steps = ['Choose a role', 'Choose your course/s', 'Create a title'];

export default function HorizontalLinearStepper() {
    const { activeStep, setActiveStep, skipped, setSkipped } = useGlobalContext()
//   const [activeStep, setActiveStep] = React.useState(0);
//   const [skipped, setSkipped] = React.useState(new Set());

// const createLearningJourneyURL = 'http://192.168.0.102:5002/createlearningjourney'

// const createLearningJourney  = async(formData) => {
//   try {
//     const requestOptions = {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify(formData)
//   };
//   fetch(createLearningJourneyURL, requestOptions)
//     .then(response => response.json())

// } catch (error) {
//     console.log(error.response)
// }
// }

  // const isStepOptional = (step) => {
  //   return step === 1;
  // };

  const isStepSkipped = (step) => {
    return skipped.has(step);
  };

  const handleNext = () => {
    let newSkipped = skipped;
    if (isStepSkipped(activeStep)) {
      newSkipped = new Set(newSkipped.values());
      newSkipped.delete(activeStep);
    }

    setActiveStep((prevActiveStep) => prevActiveStep + 1);
    setSkipped(newSkipped);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };


  // const handleReset = () => {
  //   setActiveStep(0);
  // };

  return (
    <Box sx={{ width: '100%' }}>
      <Stepper activeStep={activeStep}>
        {steps.map((label, index) => {
          const stepProps = {};
          const labelProps = {};
          if (isStepSkipped(index)) {
            stepProps.completed = false;
          }
          return (
            <Step key={label} {...stepProps}>
              <StepLabel {...labelProps}>{label}</StepLabel>
            </Step>
          );
        })}
      </Stepper>
      {activeStep === steps.length ? (
        <div></div>
      ) : (
        <React.Fragment>
          <Typography sx={{ mt: 2, mb: 1 }}>Step {activeStep + 1}</Typography>
          <Box sx={{ display: 'flex', flexDirection: 'row', pt: 2 }}>
            <Button
              color="inherit"
              disabled={activeStep === 0 }
              onClick={handleBack}
              sx={{ mr: 1 }}
            >
              Back
            </Button>
            <Box sx={{ flex: '1 1 auto' }} />
            {activeStep !== 0 && (
                <Button onClick={handleNext}>
                {activeStep === steps.length - 1 ? '' : 'Next'}
              </Button>
            )}
            
          </Box>
        </React.Fragment>
      )}
    </Box>
  );
}
