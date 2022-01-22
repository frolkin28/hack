import { createGlobalStyle } from "styled-components";
import {colors, fontFamily} from "./theme";

export const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    font-family: ${fontFamily};
    text-decoration: none;
    border: none;
    appearance: none;
    outline: none;
    box-shadow: none;
  }

  body, html, #root {
    height: 100%;
    width: 100%;
    overflow-x: hidden;
  }

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0);
    margin: 3px;
  }

  &::-webkit-scrollbar-thumb {
    background: ${colors.primary};
    border-radius: 5px;
  }

  &::-webkit-scrollbar-thumb:hover {
    background: ${colors.secondary};
  }
`;
