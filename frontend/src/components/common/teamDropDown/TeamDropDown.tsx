import styles from "./styles/teamDropDown.module.scss";

interface Props {
  team: string;
}

function TeamDropDown({ team }: Props) {
  return (
    <button className={styles.container} type="button">
      <p className={styles.team_text}>{team}</p>
      <div className={styles.drop_down_img_box}>
        <img src="/src/assets/image/dropdown.png" alt="dropdown_img" />
      </div>
    </button>
  );
}

export default TeamDropDown;
