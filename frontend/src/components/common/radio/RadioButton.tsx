import React from "react";
import styles from "./styles/radioButton.module.scss";

interface RadioButtonProps {
  label: string;
  name: string;
  value: boolean;
  checked: boolean;
  onChange: (value: boolean) => void;
}

const RadioButton: React.FC<RadioButtonProps> = ({
  label,
  name,
  value,
  checked,
  onChange,
}) => {
  return (
    <label className={styles.radioButton}>
      <input
        type="radio"
        name={name}
        value={String(value)}
        checked={checked}
        onChange={() => onChange(value)}
        className={styles.radioInput}
      />
      <span className={styles.customRadio}></span>
      <span className={styles.labelText}>{label}</span>
    </label>
  );
};

export default RadioButton;
