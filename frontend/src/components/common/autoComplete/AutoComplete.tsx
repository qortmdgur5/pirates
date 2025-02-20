import * as React from "react";
import {
  useAutocomplete,
} from "@mui/base/useAutocomplete";
import { Button } from "@mui/base/Button";
import { Popper } from "@mui/base/Popper";
import { styled } from "@mui/system";
import { unstable_useForkRef as useForkRef } from "@mui/utils";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";
import ClearIcon from "@mui/icons-material/Clear";

// AutoCompleteProps 정의
interface AutoCompleteProps {
  id: number;
  label: string;
}

interface AutocompleteProps {
  options: AutoCompleteProps[]; // options를 prop으로 받음
  setValue: React.Dispatch<React.SetStateAction<number | undefined>>; // setValue prop 추가
  disableClearable?: boolean;
  disabled?: boolean;
  readOnly?: boolean;
}

const Autocomplete = React.forwardRef(function Autocomplete(
  {
    options,
    disableClearable = false,
    disabled = false,
    readOnly = false,
    setValue,
  }: AutocompleteProps,
  ref: React.ForwardedRef<HTMLDivElement>
) {
  const {
    getRootProps,
    getInputProps,
    getPopupIndicatorProps,
    getClearProps,
    getListboxProps,
    getOptionProps,
    dirty,
    id,
    popupOpen,
    focused,
    anchorEl,
    setAnchorEl,
    groupedOptions,
  } = useAutocomplete({
    options,
    getOptionLabel: (option) => option.label, // label은 option.label로 지정
    onChange: (_, newValue) => {
      // onChange에서 선택된 항목의 id를 setValue에 전달
      if (newValue) {
        setValue(newValue.id); // 선택된 항목의 id 값을 setValue로 전달
        console.log(newValue.id);
      } else {
        setValue(undefined);
      }
    },
  });

  const hasClearIcon = !disableClearable && !disabled && dirty && !readOnly;

  const rootRef = useForkRef(ref, setAnchorEl);

  return (
    <React.Fragment>
      <StyledAutocompleteRoot
        {...getRootProps()}
        ref={rootRef}
        className={focused ? "focused" : undefined}
      >
        <StyledInput
          id={id}
          disabled={disabled}
          readOnly={readOnly}
          {...getInputProps()}
        />
        {hasClearIcon && (
          <StyledClearIndicator {...getClearProps()}>
            <ClearIcon />
          </StyledClearIndicator>
        )}
        <StyledPopupIndicator
          {...getPopupIndicatorProps()}
          className={popupOpen ? "popupOpen" : undefined}
        >
          <ArrowDropDownIcon />
        </StyledPopupIndicator>
      </StyledAutocompleteRoot>
      {anchorEl ? (
        <Popper
          open={popupOpen}
          anchorEl={anchorEl}
          slots={{
            root: StyledPopper,
          }}
          modifiers={[
            { name: "flip", enabled: false },
            { name: "preventOverflow", enabled: false },
          ]}
        >
          <StyledListbox {...getListboxProps()}>
            {(groupedOptions as typeof options).map((option, index) => {
              const optionProps = getOptionProps({ option, index });

              return (
                <StyledOption {...optionProps}>{option.label}</StyledOption>
              );
            })}

            {groupedOptions.length === 0 && (
              <StyledNoOptions>No results</StyledNoOptions>
            )}
          </StyledListbox>
        </Popper>
      ) : null}
    </React.Fragment>
  );
});

export default Autocomplete;

const blue = {
  100: "#DAECFF",
  200: "#99CCF3",
  400: "#3399FF",
  500: "#007FFF",
  600: "#0072E5",
  700: "#0059B2",
  900: "#003A75",
};

const grey = {
  50: "#F3F6F9",
  100: "#E5EAF2",
  200: "#DAE2ED",
  300: "#C7D0DD",
  400: "#B0B8C4",
  500: "#9DA8B7",
  600: "#6B7A90",
  700: "#434D5B",
  800: "#303740",
  900: "#1C2025",
};

const StyledAutocompleteRoot = styled("div")(
  ({ theme }) => `
  font-family: 'NanumSquareR', sans-serif;
  color: ${theme.palette.mode === "dark" ? grey[800] : grey[800]};
  border: 1px solid ${theme.palette.mode === "dark" ? grey[800] : grey[800]};
  display: flex;
  gap: 5px;
  padding-right: 5px;
  overflow: hidden;
  width: 100%;
  height: 2.031vw;

  &.focused {
    border-color: ${blue[400]};
    box-shadow: 0 0 0 3px ${
      theme.palette.mode === "dark" ? blue[700] : blue[200]
    };
  }

  &:hover {
    background: ${theme.palette.mode === "dark" ? grey[800] : grey[50]};
    border-color: ${theme.palette.mode === "dark" ? grey[600] : grey[300]};
  }

  &:focus-visible {
    outline: 0;
  }
`
);

const StyledInput = styled("input")(
  ({ theme }) => `
  font-size: 0.875rem;
  font-family: inherit;
  font-weight: 400;
  line-height: 1.5;
  color: ${theme.palette.mode === "dark" ? grey[300] : grey[900]};
  background: inherit;
  border: none;
  padding: 8px 12px;
  outline: 0;
  flex: 1 0 auto;
`
);

// ComponentPageTabs has z-index: 1000
const StyledPopper = styled("div")`
  position: relative;
  z-index: 1001;
  width: 16.667vw;
`;

const StyledListbox = styled("ul")(
  ({ theme }) => `
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 0.875rem;
  box-sizing: border-box;
  padding: 6px;
  margin: 12px 0;
  min-width: 320px;
  overflow: auto;
  outline: 0;
  max-height: 300px;
  z-index: 1;
  background: ${theme.palette.mode === "dark" ? grey[900] : "#fff"};
  border: 1px solid ${theme.palette.mode === "dark" ? grey[700] : grey[200]};
  color: ${theme.palette.mode === "dark" ? grey[300] : grey[900]};
  box-shadow: 0px 4px 6px ${
    theme.palette.mode === "dark" ? "rgba(0,0,0, 0.3)" : "rgba(0,0,0, 0.05)"
  };
  `
);

const StyledOption = styled("li")(
  ({ theme }) => `
  list-style: none;
  padding: 8px;
  border-radius: 8px;
  cursor: default;

  &:last-of-type {
    border-bottom: none;
  }

  &:hover {
    cursor: pointer;
  }

  &[aria-selected=true] {
    background-color: ${theme.palette.mode === "dark" ? blue[900] : blue[100]};
    color: ${theme.palette.mode === "dark" ? blue[100] : blue[900]};
  }

  &.Mui-focused,
  &.Mui-focusVisible {
    background-color: ${theme.palette.mode === "dark" ? grey[800] : grey[100]};
    color: ${theme.palette.mode === "dark" ? grey[300] : grey[900]};
  }

  &.Mui-focusVisible {
    box-shadow: 0 0 0 3px ${
      theme.palette.mode === "dark" ? blue[500] : blue[200]
    };
  }

  &[aria-selected=true].Mui-focused,
  &[aria-selected=true].Mui-focusVisible {
    background-color: ${theme.palette.mode === "dark" ? blue[900] : blue[100]};
    color: ${theme.palette.mode === "dark" ? blue[100] : blue[900]};
  }
  `
);

const StyledPopupIndicator = styled(Button)(
  ({ theme }) => `
    outline: 0;
    box-shadow: none;
    border: 0;
    border-radius: 4px;
    background-color: transparent;
    align-self: center;
    padding: 0 2px;

    &:hover {
      background-color: ${
        theme.palette.mode === "dark" ? grey[700] : blue[100]
      };
      cursor: pointer;
    }

    & > svg {
      transform: translateY(2px);
    }

    &.popupOpen > svg {
      transform: translateY(2px) rotate(180deg);
    }
  `
);

const StyledClearIndicator = styled(Button)(
  ({ theme }) => `
    outline: 0;
    box-shadow: none;
    border: 0;
    border-radius: 4px;
    background-color: transparent;
    align-self: center;
    padding: 0 2px;

    &:hover {
      background-color: ${
        theme.palette.mode === "dark" ? grey[700] : blue[100]
      };
      cursor: pointer;
    }

    & > svg {
      transform: translateY(2px) scale(0.9);
    }
  `
);

const StyledNoOptions = styled("li")`
  list-style: none;
  padding: 8px;
  cursor: default;
`;
