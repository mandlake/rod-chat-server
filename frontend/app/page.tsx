"use client";

import { useState } from "react";
import { SubmitHandler, useForm } from "react-hook-form";

type Inputs = {
  question: string;
  exampleRequired?: string;
};

export default function Home() {
  const [message, setMessage] = useState("How Can I Help You Today ?");
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<Inputs>();
  const onSubmit: SubmitHandler<Inputs> = (data) => {
    console.log("입력된 값 : " + JSON.stringify(data));
    fetch("http://localhost:8000/titanic", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json()) // JSON 형식으로 파싱
      .then((data) => {
        console.log(data);
        setMessage(data.answer); // 파싱된 데이터 콘솔 출력
      })
      .catch((error) => console.log("error:", error));
  };

  console.log(watch("question"));

  return (
    <>
      <div className="flex flex-col bg-slate-950 h-screen m-0">
        <div className="flex flex-col w-[768px] m-auto gap-10">
          <p className=" text-white text-3xl">
            {message ? message : "How Can I Help You Today ?"}
          </p>
          <form
            className="relative flex flex-row bg-slate-700"
            onSubmit={handleSubmit(onSubmit)}
          >
            <input
              className="bg-slate-700 w-[708px] h-[40px] text-slate-300 pr-[60px]"
              {...register("question")}
            />
            <button
              type="submit"
              className="absolute top-0 right-0 bg-slate-700 text-slate-300 w-[60px] h-[40px] flex items-center justify-center"
            >
              Send
            </button>
          </form>
        </div>
      </div>
    </>
  );
}
