import styled from "styled-components";

export const Button = styled("button")`
  color: #ff7b73;
  top: 0;
  cursor: pointer;
  z-index: 1;
  background-color: #fff;
  width: 10em;
  height: 3.25em;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 1500;
  border-radius: 10px;
  border: thick double #ff7b73;
  
  &:disabled {
    background-color: #cccccc;
    color: #666666;
  };
`;