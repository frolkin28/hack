import styled from "styled-components";
import {colors} from "./theme";

export const RoundButton = styled("button")`
  border-radius: 50%;
  background-color: ${colors.primary};
  border: none;
  color: white;
  width: 4em;
  height: 4em;
  cursor: pointer;
  margin-left: 5em;
  margin-right: 5em;
  
  &:hover {
    background-color: ${colors.secondary};
  }
`;