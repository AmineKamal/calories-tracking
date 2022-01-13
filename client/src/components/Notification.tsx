import * as React from 'react';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert, { AlertProps } from '@mui/material/Alert';
import { useSharedState } from '../core/Store';
import { Stack } from '@mui/material';

const Alert = React.forwardRef<HTMLDivElement, AlertProps>(function Alert(props, ref) 
{
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

export default function Notification() {
  const [state, setState] = useSharedState();
  const setOpen = (isOpen: boolean) => setState((value) => ({...value, notification: {...value.notification, isOpen}}));
  const handleClose = (_event?: React.SyntheticEvent | Event, _reason?: string) => setOpen(false);

  return (
    <Stack spacing={2} sx={{ width: '100%' }}>
      <Snackbar open={state.notification.isOpen} autoHideDuration={6000} onClose={handleClose}>
          <Alert severity={state.notification.severity} sx={{ width: '100%' }}>{state.notification.message}</Alert>
      </Snackbar>
    </Stack>
  );
}