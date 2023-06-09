import * as React from "react";
import { useState } from "react";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import axios from "axios";
import { Box, Container } from "@mui/system";
import { Typography } from "@mui/material";
import { TypeAnimation } from "react-type-animation";

const colors = {
    background: "#434654",
    sidebar: "#202123",
    primary: "#f37321",
    secondary: "#f89b6c",
    sub: "#fbb584",
};

function App() {
    const [data, setData] = useState();
    const onClick = async () => {
        const data = await axios.get("http://localhost:3001/");
        setData(data);
    };

    return (
        <div className="App">
            <Box
                sx={{
                    width: "100vw",
                    height: "100vh",
                    display: "flex",
                }}
            >
                <Box
                    as="aside"
                    sx={{ width: "250px", backgroundColor: colors.sidebar }}
                ></Box>

                <Box
                    as="main"
                    sx={{
                        backgroundColor: colors.background,
                        flex: 1,
                        color: "white",
                    }}
                >
                    {/* header */}
                    <Box
                        as="header"
                        sx={{
                            paddingY: "12px",
                        }}
                    >
                        <Typography
                            variant="h6"
                            align="center"
                            sx={{
                                textTransform: "uppercase",
                            }}
                        >
                            join v0.1
                        </Typography>
                    </Box>
                    {/*  */}

                    <Container>
                        <Box
                            sx={{
                                display: "flex",
                                justifyContent: "end",
                            }}
                        >
                            <Button variant="contained" onClick={onClick}>
                                Execute
                            </Button>
                        </Box>

                        <Box
                            sx={{
                                display: "flex",
                                gap: "12px",
                                height: "100%",
                                marginTop: "20px",
                            }}
                        >
                            {/* Slither 결과 */}
                            <Box sx={{ height: "500px", width: "50%" }}>
                                <Typography>Result</Typography>
                                <Box
                                    sx={{
                                        marginTop: "8px",
                                        height: "100%",
                                        width: "100%",
                                        backgroundColor: colors.sidebar,
                                        overflow: "auto",
                                    }}
                                >
                                    <TypeAnimation
                                        style={{
                                            whiteSpace: "pre-line",
                                            display: "block",
                                        }}
                                        sequence={[
                                            `${data && data?.data}`,
                                            1000,
                                        ]}
                                    />
                                </Box>
                            </Box>

                            {/*  */}

                            {/* Slither Description */}
                            <Box sx={{ height: "500px", width: "50%" }}>
                                <Typography>Description</Typography>
                                <Box
                                    sx={{
                                        marginTop: "8px",
                                        height: "100%",
                                        width: "100%",
                                        backgroundColor: colors.sidebar,
                                        overflowWrap: "break-word",
                                    }}
                                >
                                    <TypeAnimation
                                        style={{
                                            whiteSpace: "pre-line",
                                            display: "block",
                                        }}
                                        sequence={[
                                            `asdjfklasdjfklasdjfalksdfjalksdfjkslsdfjlkasdfjklasdjfaklsdjflaksdjfklasjakls`, // actual line-break inside string literal also gets animated in new line, but ensure there are no leading spaces
                                            1000,
                                        ]}
                                    />
                                </Box>
                            </Box>
                            {/*  */}
                        </Box>
                    </Container>
                </Box>
            </Box>
        </div>
    );
}

function BasicButtons({ onClick }) {
    return (
        <Stack spacing={2} direction="row">
            <Button variant="text" onClick={onClick}>
                Execute
            </Button>
        </Stack>
    );
}
export default App;
