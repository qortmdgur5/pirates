import { styled } from "@mui/system";
import { Tabs } from "@mui/base/Tabs";
import { TabsList as BaseTabsList } from "@mui/base/TabsList";
import { buttonClasses } from "@mui/base/Button";
import { Tab as BaseTab, tabClasses } from "@mui/base/Tab";

interface TabsProps {
  tabs: string[];
  setIsOwner: (isOwner: boolean) => void;
}

export default function TabsComponent({ tabs, setIsOwner }: TabsProps) {
  const handleTabChange = (
    _event: React.SyntheticEvent | null,
    value: string | number | null
  ) => {
    setIsOwner(value === 0); // 0번 탭이면 true (사장님), 그 외는 false (매니저)
  };

  return (
    <Tabs defaultValue={0} onChange={handleTabChange}>
      <TabsList>
        {tabs.map((tab, index) => (
          <Tab key={index} value={index}>
            {tab}
          </Tab>
        ))}
      </TabsList>
    </Tabs>
  );
}

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

const Tab = styled(BaseTab)`
  font-family: "IBM Plex Sans", sans-serif;
  color: #fff;
  cursor: pointer;
  font-size: 0.729vw;
  font-weight: 600;
  background-color: transparent;
  width: 100%;
  padding: 0.521vw 0.625vw;
  margin: 0.313vw;
  border: none;
  border-radius: 0.365vw;
  display: flex;
  justify-content: center;

  &:hover {
    background-color: ${grey[400]};
  }

  &:focus {
    color: #fff;
    outline: 3px solid ${grey[200]};
  }

  &.${tabClasses.selected} {
    background-color: #fff;
    color: ${grey[600]};
  }

  &.${buttonClasses.disabled} {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const TabsList = styled(BaseTabsList)(
  ({ theme }) => `
  min-width: 20.833vw;
  background-color: ${grey[500]};
  border-radius: 0.625vw;
  margin-bottom: 0.833vw;
  display: flex;
  align-items: center;
  justify-content: center;
  align-content: space-between;
  box-shadow: 0px 4px 30px ${
    theme.palette.mode === "dark" ? grey[900] : grey[200]
  };
  `
);
