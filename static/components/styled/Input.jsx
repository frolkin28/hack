import styled from "styled-components";

export const Input = styled("input")`
  border: 1px solid #ffffff;
  border-radius: 3px;
  padding: 10px;
  margin: 10px 6px;
  width: calc(100% - 1.5em);
  color: #f38181;
  font-weight: 500;
  
  &:focus {
    outline: none;
  }

  &::placeholder {
    color: #f38181;
  }
`;