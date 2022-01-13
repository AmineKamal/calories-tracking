import { useAction } from "../core/Api";
import { AppBar, Box, Button, IconButton, List, ListItem, Toolbar, Typography } from "@mui/material";
import { useState } from "react";
import { CheckboxElement, MultipleSelectElement, PasswordElement, RadioElement, SelectElement, SwitchElement, TextElement } from "../components/Form";
import BackIcon from "@mui/icons-material/ArrowBack"

export default function Home() {
    const username = useState("");
    const password = useState("");

    const options = [10, 15, 20] as const;
    const radio = useState<typeof options[number]>(15);
    const multiple = useState<Partial<typeof options>>([]);
    const bool = useState(false);

    const {dispatch} = useAction("login");
    const submit = () => dispatch({username: username[0], password: password[0]});

    return (
        <form>
            <Box sx={{display: 'flex', flexDirection: 'column'}}>
                <AppBar position="static" sx={{mb: 1}}>
                    <Toolbar>
                        <IconButton size="large" edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }}>
                            <BackIcon />
                        </IconButton>
                        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                            Login
                        </Typography>
                    </Toolbar>
                </AppBar>
                <TextElement state={username} name="Username"/>
                <PasswordElement state={password} name="Password" />
                {/* <RadioElement state={radio} name="Choose Any" options={options}></RadioElement>
                <SelectElement state={radio} name="Choose Any" options={options}></SelectElement>
                <MultipleSelectElement state={multiple} name="Choose many" options={options}></MultipleSelectElement>
                <CheckboxElement state={bool} name="Test" />
                <SwitchElement state={bool} name="Test" /> */}
                <Button sx={{m:1}} variant="contained" onClick={submit}>Submit</Button>
            </Box>
        </form>
    )
}

